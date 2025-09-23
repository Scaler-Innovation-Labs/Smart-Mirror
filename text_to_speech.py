import os
import requests
import logging
from pygame import mixer
import io
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the pygame mixer once when the module is loaded
try:
    mixer.init()
    logger.info("Pygame mixer initialized successfully for audio playback.")
except Exception as e:
    logger.error(f"Failed to initialize pygame mixer. Audio playback will not work. Error: {e}")

class TextToSpeech:
    def __init__(self, voice_id="21m00Tcm4TlvDq8ikWAM"): # Default voice: 'Rachel'
        """Initializes the TextToSpeech service using the ElevenLabs API."""
        self.api_key = os.getenv("ELEVENLABS_API_KEY")
        if not self.api_key:
            logger.warning("ELEVENLABS_API_KEY not found in .env file. TTS will not function.")
            return

        self.voice_id = voice_id
        self.api_url = f"https://api.elevenlabs.io/v1/text-to-speech/{self.voice_id}"
        self.headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": self.api_key
        }

    def speak(self, text: str):
        """Generates audio from text using ElevenLabs and plays it back non-blocking."""
        if not self.api_key or not mixer.get_init():
            logger.error("TTS service is not configured or mixer failed to initialize. Cannot speak.")
            return
        if not text or not text.strip():
            logger.warning("Speak function called with empty text.")
            return
        if mixer.music.get_busy():
            logger.info("Mixer is busy, stopping previous audio before playing new.")
            mixer.music.stop()

        logger.info(f"🗣️ Generating speech for: '{text}'")
        payload = {
            "text": text,
            "model_id": "eleven_multilingual_v2",
            "voice_settings": {"stability": 0.5, "similarity_boost": 0.75}
        }

        try:
            response = requests.post(self.api_url, json=payload, headers=self.headers, timeout=15)
            response.raise_for_status()

            audio_stream = io.BytesIO(response.content)
            mixer.music.load(audio_stream, "mp3")
            mixer.music.play()

        except requests.exceptions.RequestException as e:
            logger.error(f"API request to ElevenLabs failed: {e}")
        except Exception as e:
            logger.error(f"An unexpected error occurred during TTS playback: {e}")