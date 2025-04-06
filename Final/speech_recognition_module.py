import speech_recognition as sr

class SpeechRecognizer:
    def recognize_speech(self, mic_index=3):
        recognizer = sr.Recognizer()
        with sr.Microphone(device_index=mic_index) as source:
            recognizer.adjust_for_ambient_noise(source, duration=1)  # Reduce background noise
            try:
                audio = recognizer.listen(source, timeout=5)
                text = recognizer.recognize_google(audio)
                return text.lower()
            except sr.UnknownValueError:
                return None
            except sr.RequestError:
                return None
