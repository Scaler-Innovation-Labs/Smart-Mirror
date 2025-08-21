import time
import subprocess
import logging
from speech_recognition_module import SpeechRecognizer
from openai_nlp import NLPProcessor
from text_to_speech import TextToSpeech

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SmartMirror:
    def __init__(self, silence_threshold=6):
        """Initialize components and settings."""
        self.silence_threshold = silence_threshold
        self.recognizer = SpeechRecognizer()
        self.nlp = NLPProcessor()
        self.tts = TextToSpeech()
        self.active = True  

    def speak_and_log(self, message):
        """Speak and log the message."""
        logger.info(message)
        self.tts.speak(message)

    def capture_image(self, image_path="/home/smart-mirror/Pictures/captured_image.jpg"):
        """Capture image using libcamera."""
        command = ["libcamera-still", "-o", image_path]
        try:
            subprocess.run(command, check=True)
            self.speak_and_log(f"📸 Image captured successfully at: {image_path}")
            return image_path
        except subprocess.CalledProcessError as e:
            self.speak_and_log("❌ Failed to capture image. Please check the camera.")
            logger.error(f"Capture error: {e}")
            return None

    def capture_image_with_countdown(self):
        """Countdown before capturing the image."""
        for i in range(3, 0, -1):
            self.tts.speak(str(i))
            time.sleep(1)
        self.tts.speak("Smile!")
        return self.capture_image()

    def analyze_image(self, image_path):
        """Use OpenAI to analyze image clarity and key attributes."""
        return self.nlp.analyze_user_image(image_path)

    def handle_fashion_request(self, transcript, intent):
        """Handle outfit/jewelry/makeup suggestions."""
        self.speak_and_log("Got it! Let me analyze your style. Say cheese...")
        image_path = self.capture_image_with_countdown()
        if not image_path:
            self.speak_and_log("Sorry, I couldn't capture your image. Let's try again.")
            return

        analysis = self.analyze_image(image_path)
        if analysis.get("clarity") == "poor":
            self.speak_and_log("Your image is unclear. Can we try retaking it?")
            return

        wardrobe_items = self.nlp.fetch_wardrobe_items()
        if not wardrobe_items:
            self.speak_and_log("I couldn't access your wardrobe. Let's try again later.")
            return

        response = self.nlp.generate_fashion_response(
            transcript=transcript,
            image_path=image_path,
            wardrobe_urls=wardrobe_items,
            requested_categories=intent
        )
        self.speak_and_log(response)

    def get_gpt_response(self, transcript):
        """Determine intent and handle requests accordingly."""
        intent = self.nlp.detect_intent(transcript)
        logger.info(f"Detected intent: {intent}")

        if any(keyword in intent for keyword in ["outfit", "makeup", "jewelry"]):
            self.handle_fashion_request(transcript, intent)
        elif "thank you" in transcript.lower() or "done" in transcript.lower():
            self.speak_and_log("You're welcome! Ending the session.")
            self.active = False
        else:
            self.speak_and_log(self.nlp.generate_response(transcript))

    def get_transcript(self):
        """Capture speech input."""
        self.speak_and_log("I'm listening...")
        transcript = self.recognizer.recognize()
        if transcript:
            logger.info(f"User said: {transcript}")
            return transcript
        self.speak_and_log("I didn't catch that. Could you repeat?")
        return None

    def listen_for_wake_word(self, timeout=60):
        """Listen for 'Hey Mirror' or 'Hello Mirror' with timeout."""
        start_time = time.time()
        self.speak_and_log("Listening for your wake word...")
        while time.time() - start_time < timeout:
            command = self.recognizer.recognize()
            if command and ("hey mirror" in command.lower() or "hello mirror" in command.lower()):
                self.speak_and_log("Hi there! How can I assist you today?")
                return True
        logger.warning("Wake word not detected within timeout.")
        return False

    def run_once(self):
        """Run a single interaction."""
        if self.listen_for_wake_word():
            while self.active:
                transcript = self.get_transcript()
                if transcript:
                    self.get_gpt_response(transcript)
