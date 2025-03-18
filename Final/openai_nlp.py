import openai
import os
from dotenv import load_dotenv
from openai import OpenAIError  # ✅ Correct error handling import

class NLPProcessor:
    def __init__(self):
        load_dotenv()
        self.OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

        if not self.OPENAI_API_KEY:
            raise ValueError("Missing OpenAI API Key. Set it in .env file.")

        self.client = openai.OpenAI(api_key=self.OPENAI_API_KEY)  # ✅ New client initialization

    def generate_response(self, text_input):
        """Send text input to OpenAI and return response."""
        try:
            response = self.client.chat.completions.create(  # ✅ Updated API call
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": text_input}]
            )
            return response.choices[0].message.content  # ✅ New response format
        except OpenAIError as e:
            return f"⚠️ OpenAI API Error: {e}"
        except Exception as e:
            return f"⚠️ Unexpected Error: {e}"
