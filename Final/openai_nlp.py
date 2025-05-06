import openai
import os
from dotenv import load_dotenv
from openai import OpenAIError 
import requests
class NLPProcessor:
    def __init__(self):
        
        load_dotenv()
        self.OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
        if not self.OPENAI_API_KEY:
            raise ValueError("Missing OpenAI API Key. Set it in .env file.")

        self.client = openai.OpenAI(api_key=self.OPENAI_API_KEY) 


    def fetch_wardrobe_items(self):
        FASTAPI_URL = "http://localhost:8000"
        try:
            response = requests.get(f"{FASTAPI_URL}/wardrobe")
            response.raise_for_status()
            categories = response.json()
            # print(categories)
            category_names = [c["name"].strip() for c in categories]
            # print(category_names)

            for category in category_names:
                response = requests.get(f"{FASTAPI_URL}/wardrobe/{category}")
                response.raise_for_status()
                items = response.json()
                print(items)

            return items

        except requests.exceptions.RequestException as e:
            print(f"Error fetching wardrobe items: {e}")
            return None
    def generate_response(self, text_input):
        """Send text input to OpenAI and return response."""
        try:
            response = self.client.chat.completions.create( 
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": f"{text_input}"}], 
            )
            return response.choices[0].message.content  
        except OpenAIError as e:
            return f"⚠️ OpenAI API Error: {e}"
        except Exception as e:
            return f"⚠️ Unexpected Error: {e}"
        
if __name__ == "__main__":
    nlp_processor = NLPProcessor()
    nlp_processor.fetch_wardrobe_items()