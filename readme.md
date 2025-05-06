# Smart Mirror Voice Assistant

This project is a **voice-activated smart mirror assistant** that listens for the wake phrase **"Hey Mirror"**, converts speech to text, processes the request using OpenAI, and then speaks out the response.

## 📂 Project Structure
```
├── hey_mirror.py            # Listens for the wake phrase "Hey Mirror"
├── speech_to_text.py        # Converts speech to text
├── nlp_processor.py         # Processes the text with OpenAI API
├── text_to_speech.py        # Converts AI response to speech
├── requirements.txt         # Dependencies list
├── .env                     # Stores OpenAI API key (DO NOT SHARE)
├── README.md                # Project documentation
```

## 🛠️ Setup Instructions
### 1️⃣ Clone the Repository
```bash
git clone https://github.com/your-repo-name.git
cd your-repo-name
```

### 2️⃣ Install Dependencies
Ensure you have **Python 3.7+** installed, then run:
```bash
pip install -r requirements.txt
```

### 3️⃣ Set Up OpenAI API Key
1. Create a **.env** file in the project folder.
2. Add your OpenAI API key inside **.env**:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

## 🚀 How to Run the Project
### Step 1: Start the Wake Phrase Listener
This script keeps listening for **"Hey Mirror"** to activate the assistant.
```bash
python hey_mirror.py
```

### Step 2: Speech-to-Text Processing
Once activated, speech is converted into text:
```bash
python speech_to_text.py
```

### Step 3: Process the Text with OpenAI
The transcribed text is sent to OpenAI to generate a response:
```bash
python nlp_processor.py
```

### Step 4: Convert AI Response to Speech
The AI-generated response is spoken out:
```bash
python text_to_speech.py
```

## 📝 File Descriptions
### **1️⃣ `hey_mirror.py`**
- Listens for the wake phrase **"Hey Mirror"**.
- Once detected, activates speech recognition.

### **2️⃣ `speech_to_text.py`**
- Captures audio input and converts it into text using **SpeechRecognition**.

### **3️⃣ `nlp_processor.py`**
- Uses OpenAI API to generate a response based on the user's command.
- Stores conversation history for context.

### **4️⃣ `text_to_speech.py`**
- Converts the AI-generated text response into speech using **pyttsx3**.

## 🛠️ Troubleshooting
- **Microphone Not Detected?**
  - Ensure your microphone is connected and working.
  - Run `python -m speech_recognition` to test audio input.

- **OpenAI API Errors?**
  - Check that your **.env** file has the correct API key.
  - Ensure you have an active OpenAI account.

- **Speech Not Playing?**
  - Make sure `pyttsx3` is installed correctly.
  - Try running `python text_to_speech.py` separately to debug.

## 🏆 Credits
- Built using **SpeechRecognition**, **OpenAI GPT**, and **pyttsx3**.
- Developed for a **smart mirror voice assistant project**.

## 📜 License
This project is open-source under the **MIT License**.

---
🎤 **"Hey Mirror, how do I look today?"** 😎

