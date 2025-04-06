import time
from threading import Thread
import cv2
from speech_recognition_module import SpeechRecognizer
from openai_nlp import NLPProcessor
from text_to_speech import TextToSpeech
from image_nlp_processor import ImageNLPProcessor

class Camera:
    @staticmethod
    def capture_frame():
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        cv2.imwrite('image.jpg', frame)
        return 'image.jpg'

class SmartMirror:
    def __init__(self, silence_threshold=6):
        """Initialize components and settings."""
        self.silence_threshold = silence_threshold
        self.recognizer = SpeechRecognizer()  # Speech Recognition Module
        self.nlp = NLPProcessor()  # OpenAI NLP Module
        self.inp = ImageNLPProcessor() # OpenAI GPT4 Vision Preview
        self.tts = TextToSpeech()  # Text-to-Speech Module

    def listen_for_wake_word(self):
        """Continuously listen for 'Hey Mirror' and activate when detected."""
        print("🎧 Listening for 'Hey Mirror'...")
        while True:
            command = self.recognizer.recognize_speech()
            if command and "hey mirror" in command.lower():
                print("✅ Wake word detected!")
                return True

    def get_transcript(self):
        """Listen for user speech and return transcribed text."""
        print("🎙 Speak now... ")
        transcript = self.recognizer.recognize_speech()
        if transcript:
            print(f"🗣 You said: {transcript}")
            return transcript
        print("🤔 Could not understand speech.")
        return None

    def get_gpt_response(self, transcript):
        """Send user speech and image to OpenAI and get a response."""
        file_path = Camera.capture_frame()

        response = self.inp.generate_response(transcript, file_path)
        if response:
            print(f"🤖 AI Response: {response}")
            self.tts.speak(response)  # Convert AI response to speech
        return response

    def run(self):
        """Main loop to listen, process speech, and respond."""
        while True:
            if self.listen_for_wake_word():
                while True:
                    transcript = self.get_transcript()
                    if not transcript:
                        print("🛑 No response detected. Listening for 'Hey Mirror' again...")
                        break  # Exit to listen for wake word again

                    response = self.get_gpt_response(transcript)
                    if not response:
                        print("🛑 AI did not respond. Stopping conversation.")
                        break  # Stop if GPT has no response

if __name__ == "__main__":
    mirror = SmartMirror()
    mirror.run()
