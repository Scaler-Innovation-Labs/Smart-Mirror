import time
from speech_recognition_module import SpeechRecognizer
from openai_nlp import NLPProcessor
from text_to_speech import TextToSpeech

class SmartMirror:
    def __init__(self, silence_threshold=6):
        """Initialize components and settings."""
        self.silence_threshold = silence_threshold
        self.recognizer = SpeechRecognizer()  # Speech Recognition Module
        self.nlp = NLPProcessor()  # OpenAI NLP Module
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
        """Send user speech to OpenAI and get a response."""
        response = self.nlp.generate_response(transcript)
        if response:
            print(f"🤖 AI Response: {response}")
            self.tts.speak(response)  # Convert AI response to speech
        return response

    def run_once(self):
        """Run a single interaction: wake word → command → response"""
        if self.listen_for_wake_word():
            transcript = self.get_transcript()
            if not transcript:
                return None, None

            response = self.get_gpt_response(transcript)
            return transcript, response
        return None, None
