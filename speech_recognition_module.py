import os
import tempfile
import logging
import openai
import speech_recognition as sr
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

class SpeechRecognizer:
    def __init__(self, energy_threshold=4000, pause_threshold=1.5):
        """Initializes the speech recognizer with Whisper."""
        self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.recognizer = sr.Recognizer()
        self.recognizer.energy_threshold = energy_threshold
        self.recognizer.pause_threshold = pause_threshold

        try:
            self.microphone = sr.Microphone()
            with self.microphone as source:
                logger.info("Calibrating microphone for ambient noise...")
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
            logger.info("Microphone calibrated.")
        except Exception as e:
            logger.error(f"No microphone found or microphone error: {e}")
            self.microphone = None

    def recognize(self):
        """Records audio from the microphone and transcribes it using the Whisper API."""
        if not self.microphone:
            logger.error("Cannot recognize speech, no microphone available.")
            return None

        try:
            with self.microphone as source:
                logger.info("Listening for command...")
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=15)

            with tempfile.NamedTemporaryFile(suffix=".wav", delete=True) as temp_audio_file:
                temp_audio_file.write(audio.get_wav_data())
                temp_audio_file.seek(0) # Rewind the file to the beginning

                with open(temp_audio_file.name, "rb") as audio_file:
                    transcription = self.client.audio.transcriptions.create(
                        model="whisper-1",
                        file=audio_file,
                        language="en"
                    )
            return transcription.text

        except sr.WaitTimeoutError:
            logger.warning("Listening timed out while waiting for phrase to start.")
            return None
        except openai.APIError as e:
            logger.error(f"OpenAI API error during transcription: {e}")
            return None
        except Exception as e:
            logger.error(f"An unexpected error occurred during speech recognition: {e}")
            return None