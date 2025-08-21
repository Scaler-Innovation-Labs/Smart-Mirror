import os
import sys
import speech_recognition as sr
import logging
from contextlib import contextmanager

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
        self.recognizer = sr.Recognizer()
        # Set custom thresholds for speech recognition
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 1.2   # Allow short pauses without stopping
        self.recognizer.energy_threshold = 300

        # Suppress ALSA/JACK logs during microphone access
        with suppress_stderr():
            mic_list = sr.Microphone.list_microphone_names()
        logger.info("Available Microphones:")
        for index, name in enumerate(mic_list):
            logger.info(f"  [{index}] {name}")
        
        self.device_index = self.find_usb_microphone_index()

        with suppress_stderr():
            self.microphone = sr.Microphone(device_index=self.device_index)

        with suppress_stderr():
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
        logger.info("Calibrated microphone for ambient noise.")

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
            logger.info("Listening... (speak now)")
            with suppress_stderr():
                with self.microphone as source:
                    self.recognizer.adjust_for_ambient_noise(source, duration=2)
                    audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
            result = self.recognizer.recognize_google(audio).lower()

            logger.info(f"Recognized: {result}")
            return result

        except sr.WaitTimeoutError:
            logger.warning("Timeout: No speech detected.")
        except sr.UnknownValueError:
            logger.warning("Google could not understand the audio.")
        except sr.RequestError as e:
            logger.error(f"Google request failed: {e}")
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
        return None
