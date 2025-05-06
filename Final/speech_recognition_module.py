import os
import speech_recognition as sr
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("SmartMirror")

class SpeechRecognizer:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.audio_file = "recording.wav"
        self.recording_command = (
            "arecord -D plughw:3,0 -f S16_LE -r 16000 -d 5 {}".format(self.audio_file)
        )
    def _cleanup(self):
        """Remove temporary audio files"""
        if os.path.exists(self.audio_file):
            os.remove(self.audio_file)
    
    def recognize(self):
        """Record and recognize speech"""
        try:
            # Record audio
            logger.info("Recording... (speak now)")
            os.system(self.recording_command)
            
            # Process recording
            with sr.AudioFile(self.audio_file) as source:
                audio = self.recognizer.record(source)
                result = self.recognizer.recognize_google(audio).lower()
                logger.info(f"Recognized: {result}")
                return result
                
        except sr.UnknownValueError:
            logger.warning("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            logger.error(f"Could not request results; {e}")
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
        finally:
            self._cleanup()
        return None

# if __name__ == "__main__":
#     recognizer = SpeechRecognizer()
#     print("Speak after the beep...")
#     result = recognizer.recognize()
#     print(f"You said: {result}" if result else "No speech detected")