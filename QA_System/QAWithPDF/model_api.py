import os
import sys
from dotenv import load_dotenv
from llama_index.llms.google_genai import GoogleGenAI
from exception import customexception
from logger import logging

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

def load_model():
    """Loads a Gemini model for natural language processing using LlamaIndex.
    Returns:
    - GoogleGenAI: An instance of the GoogleGenAI class initialized with 'gemini-3.8-flash'."""
    try:
        model = GoogleGenAI(model="gemini-3.7-flash", api_key=GOOGLE_API_KEY)
        return model
    except Exception as e:
        raise customexception(e, sys)