import os
import sys
import speech_recognition as sr
import logging
from contextlib import contextmanager
import openai
import tempfile
from dotenv import load_dotenv
load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("SmartMirror")

@contextmanager
def suppress_stderr():
    """Temporarily suppress C-level stderr (ALSA, JACK warnings)"""
    fd = sys.stderr.fileno()
    old_stderr = os.dup(fd)
    with open(os.devnull, 'w') as devnull:
        os.dup2(devnull.fileno(), fd)
    try:
        yield
    finally:
        os.dup2(old_stderr, fd)
        os.close(old_stderr)

class SpeechRecognizer:
    def __init__(self):
        self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def find_usb_microphone_index(self):
        with suppress_stderr():
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
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=7)

            # Save temp wav file
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
