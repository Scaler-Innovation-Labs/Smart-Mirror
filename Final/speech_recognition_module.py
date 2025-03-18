import speech_recognition as sr

class SpeechRecognizer:
    def __init__(self):
        self.recognizer = sr.Recognizer()

    def recognize_speech(self):
        """Capture audio and return recognized text."""
        with sr.Microphone() as source:
            print("🎙 Speak now... ")
            self.recognizer.adjust_for_ambient_noise(source)
            audio = self.recognizer.listen(source)

        try:
            return self.recognizer.recognize_google(audio).strip()
        except sr.UnknownValueError:
            print("🤔 Could not understand the audio.")
            return None
        except sr.RequestError as e:
            print(f"⚠️ Google Speech Recognition error: {e}")
            return None
