import os
import sys
import tempfile
import logging
import openai
import speech_recognition as sr
from contextlib import contextmanager
from dotenv import load_dotenv
load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("SmartMirror")

@contextmanager
def suppress_stderr():
    """Temporarily suppress C-level stderr (ALSA, JACK warnings)."""
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
        self.recognizer = sr.Recognizer()

        with suppress_stderr():
            mic_list = sr.Microphone.list_microphone_names()
        logger.info("Available Microphones:")
        for i, name in enumerate(mic_list):
            logger.info(f"[{i}] {name}")

        self.device_index = self.find_usb_microphone_index()

        with suppress_stderr():
            self.microphone = sr.Microphone(device_index=self.device_index)

        with suppress_stderr():
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
        logger.info("Microphone calibrated for ambient noise.")

    def find_usb_microphone_index(self):
        with suppress_stderr():
            mic_list = sr.Microphone.list_microphone_names()
        for index, name in enumerate(mic_list):
            if "usb" in name.lower() or "pnp" in name.lower():
                logger.info(f"USB mic found at index {index}: {name}")
                return index
        logger.warning("USB mic not found, defaulting to index 0.")
        return 0

    def recognize(self):
        """Record audio and transcribe using Whisper API."""
        try:
            with suppress_stderr():
                with self.microphone as source:
                    logger.info("Listening...")
                    audio = self.recognizer.listen(source, timeout=10, phrase_time_limit=10)

            # Save temp audio
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
                f.write(audio.get_wav_data())
                temp_filename = f.name

            with open(temp_filename, "rb") as audio_file:
                transcription = self.client.audio.transcriptions.create(
                    model="whisper-1", 
                    file=audio_file,
                    language= "en"
                )

            return transcription.text.lower()
        except Exception as e:
            logger.error(f"Whisper recognition failed: {e}")
            return None
