import speech_recognition as sr

def find_bluetooth_mic(name_hint="bcm2835 Headphones"):
    for index, name in enumerate(sr.Microphone.list_microphone_names()):
        print(f"Device {index}: {name}")  # List all devices
        if name_hint.lower() in name.lower():
            return index
    return None

# Automatically get the Bluetooth microphone index
bt_mic_index = find_bluetooth_mic()
if bt_mic_index is None:
    print("❌ Bluetooth mic not found.")
else:
    print(f"✅ Using Bluetooth mic at index {bt_mic_index}")

class SpeechRecognizer:
    def recognize_speech(self):
        recognizer = sr.Recognizer()
        if bt_mic_index is None:
            return "Bluetooth mic not found. Please check the connection."

        with sr.Microphone(device_index=bt_mic_index) as source:
            recognizer.adjust_for_ambient_noise(source, duration=1)  # Reduce background noise
            try:
                print("Listening...")
                audio = recognizer.listen(source, timeout=5)
                print("Recognizing...")
                text = recognizer.recognize_google(audio)
                return text.lower()
            except sr.UnknownValueError:
                return "Google Speech Recognition could not understand the audio"
            except sr.RequestError as e:
                return f"Could not request results from Google Speech Recognition service; {e}"
