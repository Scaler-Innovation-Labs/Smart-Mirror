import os
import speech_recognition as sr
import openai
import tempfile
import logging
from contextlib import contextmanager

logger = logging.getLogger("SpeechRecognizer")

class SpeechRecognizer:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.mic_index = self.find_usb_microphone_index()
        self.microphone = sr.Microphone(device_index=self.mic_index)  # <-- missing before
        self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def find_usb_microphone_index(self):
        mic_list = sr.Microphone.list_microphone_names()
        for index, name in enumerate(mic_list):
            if "usb" in name.lower() or "pnp" in name.lower():
                logger.info(f"USB mic found at index {index}: {name}")
                return index
        logger.warning("USB mic not found, using default index 0")
        return 0

    def recognize(self):
        try:
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                logger.info("🎤 Listening...")
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=7)

            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
                f.write(audio.get_wav_data())
                temp_filename = f.name

            # Whisper transcription
            with open(temp_filename, "rb") as audio_file:
                transcript = self.client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file
                )
            return transcript.text.lower()

        except Exception as e:
            logger.error(f"Whisper failed: {e}")
            return None
