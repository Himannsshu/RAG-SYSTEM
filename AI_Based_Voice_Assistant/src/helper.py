import os
import speech_recognition as sr
from dotenv import load_dotenv
from google import genai
from gtts import gTTS

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
client = genai.Client(api_key=GOOGLE_API_KEY)
def voice_input():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=1)
        print("listening...")
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=10)
        except sr.WaitTimeoutError:
            print("no speech detected")
            return None
    try:
        text = r.recognize_google(audio)
        print("you said: ", text)
        return text
    except sr.UnknownValueError:
        print("sorry, could not understand the audio")
    except sr.RequestError as e:
        print("could not request result from google speech recognition service: {0}".format(e))
    return None
    
def text_to_speech(text):
    tts=gTTS(text=text, lang="en")
    tts.save("speech.mp3")

def llm_model_object(user_text):
    response = client.models.generate_content(model="gemini-3.5-flash",contents=user_text)
    return response.text
