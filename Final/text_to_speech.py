import pyttsx3

class TextToSpeech:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.engine.setProperty("rate", 160)
        self.engine.setProperty("volume", 1.0)

    def speak(self, text):
        """Convert text to speech and speak it."""
        print(f"🗣 Speaking: {text}")
        self.engine.say(text)
        self.engine.runAndWait()
