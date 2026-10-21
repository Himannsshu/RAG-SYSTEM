import os
import json
import shutil
import speech_recognition as sr
from dotenv import load_dotenv
from moviepy import VideoFileClip, AudioFileClip
from pytubefix import YouTube
from llama_index.core import Settings, SimpleDirectoryReader, StorageContext
from llama_index.core.indices import MultiModalVectorStoreIndex
from llama_index.core.llms import ChatMessage, ImageBlock, TextBlock
from llama_index.core.schema import ImageNode
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.google_genai import GoogleGenAI
from llama_index.vector_stores.lancedb import LanceDBVectorStore

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

VIDEO_URL = "https://youtu.be/3dhcmeOTZ_Q"
QUERY = "can you tell me what is linear regression and the equation of multiple linear regression?"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VIDEO_DIR = os.path.join(BASE_DIR, "video_data")
DATA_DIR = os.path.join(BASE_DIR, "mixed_data")
LANCEDB_DIR = os.path.join(BASE_DIR, "lancedb")
VIDEO_FILE = os.path.join(VIDEO_DIR, "input_vid.mp4")
RAW_AUDIO_FILE = os.path.join(VIDEO_DIR, "input_audio.mp4")
AUDIO_FILE = os.path.join(DATA_DIR, "output_audio.wav")

os.makedirs(VIDEO_DIR, exist_ok=True)
os.makedirs(DATA_DIR, exist_ok=True)

yt = YouTube(VIDEO_URL)
metadata = {"Author": yt.author, "Title": yt.title, "Views": yt.views}

video_streams = yt.streams.filter(adaptive=True, only_video=True, file_extension="mp4")
usable = [s for s in video_streams if s.resolution and int(s.resolution.rstrip("p")) <= 720]
h264 = [s for s in usable if (s.video_codec or "").startswith("avc1")]
pool = h264 or usable or list(video_streams)
video_stream = max(pool, key=lambda s: int(s.resolution.rstrip("p")))
video_stream.download(output_path=VIDEO_DIR, filename="input_vid.mp4")
yt.streams.get_audio_only().download(output_path=VIDEO_DIR, filename="input_audio.mp4")

clip = VideoFileClip(VIDEO_FILE)
clip.write_images_sequence(os.path.join(DATA_DIR, "frame%04d.png"), fps=0.2)
clip.close()

audio_clip = AudioFileClip(RAW_AUDIO_FILE)
audio_clip.write_audiofile(AUDIO_FILE, fps=16000, ffmpeg_params=["-ac", "1"])
audio_clip.close()

recognizer = sr.Recognizer()
with sr.AudioFile(AUDIO_FILE) as source:
    audio_data = recognizer.record(source)
try:
    transcript = recognizer.recognize_whisper(audio_data, model="base")
except sr.UnknownValueError:
    transcript = ""
with open(os.path.join(DATA_DIR, "output_text.txt"), "w", encoding="utf-8") as f:
    f.write(transcript)
os.remove(AUDIO_FILE)

Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
shutil.rmtree(LANCEDB_DIR, ignore_errors=True)
storage_context = StorageContext.from_defaults(
    vector_store=LanceDBVectorStore(uri=LANCEDB_DIR, table_name="text_collection"),
    image_store=LanceDBVectorStore(uri=LANCEDB_DIR, table_name="image_collection"),
)
documents = SimpleDirectoryReader(DATA_DIR).load_data()
index = MultiModalVectorStoreIndex.from_documents(documents, storage_context=storage_context)
retriever = index.as_retriever(similarity_top_k=1, image_similarity_top_k=5)

images, texts = [], []
for node in retriever.retrieve(QUERY):
    if isinstance(node.node, ImageNode):
        images.append(node.node.metadata["file_path"])
    else:
        texts.append(node.text)

prompt = (
    "Based on the provided information, including relevant images and retrieved context "
    "from the video, accurately and precisely answer the query without any additional "
    "prior knowledge.\n"
    f"Context: {''.join(texts)}\n"
    f"Metadata for video: {json.dumps(metadata)}\n"
    f"Query: {QUERY}\n"
    "Answer: "
)
blocks = [TextBlock(text=prompt)] + [ImageBlock(path=p, image_mimetype="image/png") for p in images]
llm = GoogleGenAI(model="gemini-3.5-flash", api_key=GOOGLE_API_KEY)
print(llm.chat([ChatMessage(role="user", blocks=blocks)]).message.content)