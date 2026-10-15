#  Multilingual AI Assistant

A voice-based AI assistant built with Streamlit. Click a button, speak your question, and the app transcribes your voice, gets an answer from Google's Gemini model, shows the response as text, and reads it aloud. You can also download the spoken answer as an MP3 file.

##  Features

- Voice input through your microphone (speech-to-text)
- AI-generated answers using Google Gemini
- Spoken replies using text-to-speech (gTTS)
- Audio playback and MP3 download inside the app
- Simple web interface built with Streamlit

##  Tech Stack

- **Python**
- **Streamlit** – web interface
- **Google Generative AI (Gemini)** – language model
- **SpeechRecognition** – speech-to-text
- **gTTS (Google Text-to-Speech)** – text-to-speech
- **python-dotenv** – loads the API key from a `.env` file

##  Prerequisites

- Python 3.9 or higher
- A Google API key from [Google AI Studio](https://aistudio.google.com/)

## 🚀 How to Run

### Step 1: Clone the repository

```bash
git clone https://github.com/<your-username>/<your-repo-name>.git
cd <your-repo-name>
```

### Step 2: Create and activate a virtual environment

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

Mac / Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install PyAudio dependencies (needed for the microphone)

- **Windows:** no extra step is usually needed. If `pyaudio` fails to install, run:
```bash
  pip install pipwin
  pipwin install pyaudio
```
- **Mac:**
```bash
  brew install portaudio
```
- **Linux (Ubuntu/Debian):**
```bash
  sudo apt install portaudio19-dev python3-dev
```

### Step 4: Install the requirements

```bash
pip install -r requirements.txt
```

### Step 5: Add your API key

Create a `.env` file in the root folder of the project and add:

```env
GOOGLE_API_KEY="your_google_api_key_here"
```

### Step 6: Run the app

```bash
streamlit run app.py
```

Then open this address in your browser:

```
http://localhost:8501
```

##  How to Use

1. Click the **Ask me anything** button.
2. Speak your question when the app says "Listening...".
3. Read the response in the text box, listen to the audio, or download the MP3.


## Changing the Language

The app currently listens and speaks in English. To use another language, change the language codes in `src/helper.py`:

- Speech recognition: `r.recognize_google(audio, language="hi-IN")`
- Text-to-speech: `gTTS(text=text, lang="hi")`
