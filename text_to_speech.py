import os
import requests
import subprocess
import tempfile
import pyttsx3
from dotenv import load_dotenv
load_dotenv()

class TextToSpeech:
    def __init__(self):
        self.api_key = os.getenv("ELEVENLABS_API_KEY")
        self.voice_id = "en-US-natalie"
        self.engine = pyttsx3.init()
        self.engine.setProperty("rate", 160)
        self.engine.setProperty("volume", 1.0)

    def speak(self, text):
        print(f"🗣 Speaking: {text}")
        if self.api_key:
            try:
                url = f"https://api.elevenlabs.io/v1/text-to-speech/{self.voice_id}"
                headers = {"xi-api-key": self.api_key}
                response = requests.post(url, headers=headers, json={"text": text})

                if response.status_code == 200:
                    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as f:
                        f.write(response.content)
                        temp_filename = f.name
                    subprocess.run(["mpg123", temp_filename])
                    return
            except Exception as e:
                print(f"⚠️ ElevenLabs TTS failed, falling back: {e}")

        # Fallback: pyttsx3
        self.engine.say(text)
        self.engine.runAndWait()
