import speech_recognition as sr
import time
from speech_recognition_module import SpeechRecognizer
from openai_nlp import NLPProcessor
from text_to_speech import TextToSpeech

class SmartMirror:
    def __init__(self, silence_threshold=6):
        self.listener = sr.Recognizer()
        self.silence_threshold = silence_threshold
        self.recognizer = SpeechRecognizer()
        self.nlp = NLPProcessor()
        self.tts = TextToSpeech()

    def listen_for_wake_word(self):
        """Continuously listen for 'Hey Mirror' and activate when detected."""
        with sr.Microphone() as source:
            print("🎧 Listening for 'Hey Mirror'...")
            self.listener.adjust_for_ambient_noise(source)
            audio = self.listener.listen(source)

            try:
                command = self.listener.recognize_google(audio).lower()
                if "hey mirror" in command:
                    print("✅ Wake word detected!")
                    return True
            except sr.UnknownValueError:
                print("🤔 Could not understand.")
            except sr.RequestError as e:
                print(f"⚠️ Google Speech Recognition error: {e}")
        return False

    def get_transcript(self):
        """Listen and transcribe user's command."""
        with sr.Microphone() as source:
            print("🎙 Speak now... ")
            self.listener.adjust_for_ambient_noise(source)
            audio = self.listener.listen(source, timeout=self.silence_threshold)
            try:
                transcript = self.listener.recognize_google(audio).strip()
                print(f"🗣 You said: {transcript}")
                return transcript
            except sr.UnknownValueError:
                print("🤔 Could not understand speech.")
            except sr.RequestError as e:
                print(f"⚠️ Speech recognition error: {e}")
        return None

    def get_gpt_response(self, transcript):
        """Send the transcript to GPT and get a response."""
        response = self.nlp.generate_response(transcript)
        if response:
            print(f"🤖 AI Response: {response}")
            self.tts.speak(response)
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
