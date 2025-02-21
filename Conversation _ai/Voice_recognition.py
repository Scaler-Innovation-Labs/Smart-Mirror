import speech_recognition as sr
import time



class VoiceRecognizer:
    def __init__(self, silence_threshold=6, pause_threshold=3):
        self.recognizer = sr.Recognizer()
        self.silence_threshold = silence_threshold  
        self.pause_threshold = pause_threshold  
        self.transcript = ""

    def listen(self, source):
        """Listen for speech and return audio."""
        print("🎧 Listening...")
        return self.recognizer.listen(source, timeout=6, phrase_time_limit=None)

    def transcribe_audio(self, audio):
        """Transcribe audio using Google Speech Recognition."""
        try:
            return self.recognizer.recognize_google(audio).strip()
        except sr.UnknownValueError:
            print("🤔 Could not understand the audio.")
        except sr.RequestError as e:
            print(f"⚠️ Google Speech Recognition error: {e}")
        return None

    def recognize_speech(self):
        """Continuously listens and transcribes speech, handling pauses and long silence."""
        self.transcript = ""

        with sr.Microphone() as source:
            print("🎙 Speak now... ")
            self.recognizer.adjust_for_ambient_noise(source, duration=1)

            last_speech_time = time.time()
            print(last_speech_time)

            try:
                while True:
                    audio = self.listen(source)
                    text = self.transcribe_audio(audio)

                    if text:
                        self.transcript += " " + text
                        print(f"🗣 You said: {text}")
                        last_speech_time = time.time()  # Reset silence timer

                    # Check silence duration
                    silence_duration = time.time() - last_speech_time
                    print(silence_duration)

                    if silence_duration >= self.silence_threshold:
                        print("🛑 Stopping due to prolonged silence.")
                        break
                    
                    elif silence_duration >= self.pause_threshold:
                        if not self.transcript.endswith("[PAUSE] "):
                            self.transcript += " [PAUSE] "
                            print("⏸ Detected a pause.")

            except Exception as e:
                print(f"🔴 Error: {e}")

        print("\nFinal Transcript:", self.transcript)

if __name__ == "__main__":
    recognizer = VoiceRecognizer()
    recognizer.recognize_speech()
