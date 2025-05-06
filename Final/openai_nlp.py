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
            all_image_urls = []
            for category in category_names:
                response = requests.get(f"{FASTAPI_URL}/wardrobe/{category}")
                response.raise_for_status()
                items = response.json()
                for item in items:
                    url = item.get("image_url", "").strip()
                    if url.startswith("http"):
                        all_image_urls.append(url)

            return all_image_urls

        except requests.exceptions.RequestException as e:
            print(f"Error fetching wardrobe items: {e}")
            return None

    def generate_response_with_images(self, text_input, image_urls):
        """Send text + image URLs to OpenAI GPT-4 Vision."""
        try:
            image_contents = [
                {
                    "type": "image_url",
                    "image_url": {
                        "url": url
                    }
                }
                for url in image_urls
            ]

            messages = [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": text_input},
                        *image_contents
                    ]
                }
            ]

            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                max_tokens=1000,
            )

            return response.choices[0].message.content

        except OpenAIError as e:
            return f"⚠️ OpenAI API Error: {e}"
        except Exception as e:
            return f"⚠️ Unexpected Error: {e}"
            
if __name__ == "__main__":
    nlp_processor = NLPProcessor()
    image_urls = nlp_processor.fetch_wardrobe_items()

    user_prompt = "Suggest only one stylish outfit using these wardrobe items for a party"
    result = nlp_processor.generate_response_with_images(user_prompt, image_urls)
    print(result)