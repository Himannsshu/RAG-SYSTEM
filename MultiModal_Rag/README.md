# Multimodal Video RAG (Gemini)

Ask questions about a YouTube video and get answers based on both what is said (transcript) and what is shown (video frames), powered by Google Gemini.

## How It Works

1. Downloads a YouTube video
2. Extracts frames every 5 seconds and transcribes the audio with Whisper
3. Indexes the transcript text (HuggingFace embeddings) and frames (CLIP embeddings) in LanceDB using LlamaIndex
4. Retrieves the most relevant transcript text and frames for your question
5. Sends them to Gemini to generate the answer

## Tech Stack

- Python
- LlamaIndex
- LanceDB
- Google Gemini (`gemini-3.5-flash`)
- HuggingFace embeddings (`BAAI/bge-small-en-v1.5`) for text
- CLIP for images
- Whisper (speech-to-text)
- MoviePy, PyTube

## Requirements

- Python 3.9+
- FFmpeg installed
- Google Gemini API key (get one from Google AI Studio)

## Installation

```bash
git clone https://github.com/<your-username>/multimodal-video-rag.git
cd multimodal-video-rag
pip install "moviepy<2.0" pytube SpeechRecognition openai-whisper Pillow matplotlib python-dotenv
pip install llama-index lancedb llama-index-vector-stores-lancedb llama-index-embeddings-clip
pip install llama-index-llms-google-genai llama-index-embeddings-huggingface
pip install git+https://github.com/openai/CLIP.git
```

## Setup

Create a `.env` file in the project folder:

```
GOOGLE_API_KEY=your_api_key_here
```

Open `multimodal_video_rag.py` and set:

- `VIDEO_URL` to the YouTube video you want to use
- `QUERY` to your question
- the folder paths, if you are not running on Google Colab

## Usage

```bash
python multimodal_video_rag.py
```

The script prints the answer and shows the retrieved video frames.

## Notes

- Delete the `lancedb` folder before re-running to avoid duplicate data.
- If the YouTube download fails, try `pytubefix` or `yt-dlp` instead of `pytube`.
- If you get a "model not found" error, check the current model names in the Gemini API docs and update the model name in the script.
