import os
import time
import subprocess
import logging
from speech_recognition_module import SpeechRecognizer
from openai_nlp import NLPProcessor
from text_to_speech import TextToSpeech
import pvporcupine
from pvrecorder import PvRecorder
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Fetch and validate Picovoice Access Key
PICOVOICE_ACCESS_KEY = os.getenv("PICOVOICE_ACCESS_KEY")
if not PICOVOICE_ACCESS_KEY:
    raise ValueError("PICOVOICE_ACCESS_KEY environment variable not set in .env file!")

class SmartMirror:
    def __init__(self):
        """Initialize all components of the smart mirror."""
        logger.info("Initializing Smart Mirror components...")
        self.recognizer = SpeechRecognizer()
        self.nlp = NLPProcessor()
        self.tts = TextToSpeech()
        self.active = True
        logger.info("Smart Mirror components initialized.")

    def speak_and_log(self, message):
        """Log a message and speak it using the TTS engine."""
        logger.info(f"AI Response: {message}")
        self.tts.speak(message)

    def capture_image(self, image_path="/home/pi/Pictures/captured_image.jpg"):
        """Capture an image using libcamera-still command."""
        logger.info("Capturing image...")
        # Ensure the directory exists
        os.makedirs(os.path.dirname(image_path), exist_ok=True)
        command = ["libcamera-still", "-o", image_path, "--nopreview", "-t", "500"]
        try:
            subprocess.run(command, check=True, capture_output=True, text=True)
            logger.info(f"Image captured successfully and saved to {image_path}")
            return image_path
        except subprocess.CalledProcessError as e:
            self.speak_and_log("I'm having trouble with the camera. Please make sure it's connected properly.")
            logger.error(f"Failed to capture image. Error: {e.stderr}")
            return None
        except FileNotFoundError:
            self.speak_and_log("The camera command was not found. Please ensure libcamera-utils is installed.")
            logger.error("`libcamera-still` command not found.")
            return None


    def capture_image_with_countdown(self):
        """Perform a countdown and then capture an image."""
        self.speak_and_log("Get ready for your photo!")
        for i in range(3, 0, -1):
            self.tts.speak(str(i))
            time.sleep(1.2) # Give a bit more time for speech
        self.speak_and_log("Smile!")
        time.sleep(0.5)
        return self.capture_image()

    def handle_fashion_request(self, transcript, intent):
        """Handle a fashion-related request by capturing and analyzing an image."""
        self.speak_and_log("Of course! To give you the best advice, I'll need to take a quick photo.")
        image_path = self.capture_image_with_countdown()
        if not image_path:
            return

        self.speak_and_log("Thanks! Analyzing your style and checking your wardrobe now...")
        analysis = self.nlp.analyze_user_image(image_path)
        if analysis.get("gender") == "unknown":
            self.speak_and_log("I had a little trouble analyzing the photo. Let's try that one more time.")
            return

        wardrobe_items = self.nlp.fetch_wardrobe_items()
        if wardrobe_items is None:
            self.speak_and_log("I'm having trouble connecting to your wardrobe database right now.")
            return

        response = self.nlp.generate_fashion_response(
            transcript=transcript,
            image_path=image_path,
            wardrobe_urls=wardrobe_items,
            requested_categories=intent,
            user_analysis=analysis
        )
        self.speak_and_log(response)

    def get_gpt_response(self, transcript):
        """Determine user intent and generate an appropriate response."""
        if not transcript:
            return

        # Simple exit condition
        if any(phrase in transcript.lower() for phrase in ["goodbye", "stop", "that's all"]):
            self.speak_and_log("Goodbye!")
            self.active = False
            return

        intent = self.nlp.detect_intent(transcript)
        logger.info(f"Detected intent: {intent}")

        if any(keyword in intent for keyword in ["outfit", "makeup", "jewelry"]):
            self.handle_fashion_request(transcript, intent)
        else:
            response = self.nlp.generate_general_response(transcript)
            self.speak_and_log(response)

    def get_transcript(self):
        """Capture and transcribe user's speech."""
        self.speak_and_log("I'm listening.")
        transcript = self.recognizer.recognize()
        if transcript:
            logger.info(f"User said: {transcript}")
            return transcript
        
        self.speak_and_log("I didn't quite catch that. Could you say it again?")
        return None

    def handle_interaction(self):
        """Handles a single, complete interaction after the wake word is detected."""
        transcript = self.get_transcript()
        if transcript:
            self.get_gpt_response(transcript)
        # After one interaction, the main loop will listen for the wake word again.

    def run(self):
        """The main application loop: listens for wake word, then handles interaction."""
        try:
            porcupine = pvporcupine.create(
                access_key=PICOVOICE_ACCESS_KEY,
                keywords=['hey mirror', 'hello mirror']
            )
            recorder = PvRecorder(device_index=-1, frame_length=porcupine.frame_length)
        except pvporcupine.PorcupineError as e:
            logger.error(f"Failed to initialize Porcupine: {e}")
            self.speak_and_log("I'm having a problem with my wake word engine. Please check the logs.")
            return

        logger.info("Smart Mirror is running... Listening for wake word ('Hey Mirror' or 'Hello Mirror').")
        self.speak_and_log("I'm ready when you are. Just say 'Hey Mirror'.")

        try:
            while self.active:
                recorder.start()
                while self.active:
                    pcm = recorder.read()
                    result = porcupine.process(pcm)
                    if result >= 0:
                        logger.info(f"Wake word detected (keyword index {result})!")
                        recorder.stop()
                        self.speak_and_log("Hi there! How can I help?")
                        self.handle_interaction()
                        logger.info("Interaction finished. Listening for wake word again...")
                        break # Break from inner loop to restart recorder
        except KeyboardInterrupt:
            logger.info("Shutting down Smart Mirror.")
        finally:
            if 'recorder' in locals() and recorder is not None:
                recorder.delete()
            if 'porcupine' in locals() and porcupine is not None:
                porcupine.delete()