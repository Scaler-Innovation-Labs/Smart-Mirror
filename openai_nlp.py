import os
import base64
import requests
from dotenv import load_dotenv
import openai
from openai import OpenAIError

class NLPProcessor:
    def __init__(self):
        load_dotenv()
        self.OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
        if not self.OPENAI_API_KEY:
            raise ValueError("Missing OpenAI API Key.")
        self.client = openai.OpenAI(api_key=self.OPENAI_API_KEY)

    def encode_image(self, image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")

    def detect_intent(self, prompt):
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system",
                     "content": "Classify requests strictly into: outfit, makeup, jewelry, or general."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0,
                max_tokens=20
            )
            return response.choices[0].message.content.lower().strip()
        except Exception:
            return "general"

    def fetch_wardrobe_items(self):
        FASTAPI_URL = "http://localhost:8000"
        try:
            response = requests.get(f"{FASTAPI_URL}/wardrobe")
            response.raise_for_status()
            categories = response.json()
            urls = []
            for c in categories:
                cat = c["name"].strip()
                r = requests.get(f"{FASTAPI_URL}/wardrobe/{cat}")
                r.raise_for_status()
                urls.extend([item["image_url"].strip() for item in r.json() if item.get("image_url", "").startswith("http")])
            return urls
        except requests.exceptions.RequestException:
            return None

    def analyze_user_image(self, image_path):
        """Analyze clarity, skin tone, and hair type."""
        base64_image = self.encode_image(image_path)
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system",
                     "content": "Analyze the image. Detect clarity, skin tone, hair texture. Respond as JSON with keys: clarity (good/poor), skin_tone, hair_texture."},
                    {"role": "user",
                     "content": [{"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}]}
                ],
                max_tokens=200
            )
            import json
            return json.loads(response.choices[0].message.content)
        except Exception:
            return {"clarity": "poor"}

    def generate_response(self, prompt):
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a helpful smart mirror assistant."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300
            )
            return response.choices[0].message.content
        except OpenAIError:
            return "I had an issue processing your request."

    def generate_fashion_response(self, transcript, image_path, wardrobe_urls, requested_categories):
        base64_image = self.encode_image(image_path)
        category_map = {
            "outfit": "suggest clothing combinations",
            "jewelry": "suggest accessories that match",
            "makeup": "suggest makeup styles"
        }
        categories = [category_map[c] for c in requested_categories.split(",") if c in category_map]
        system_prompt = (
            f"You are a fashion expert. Only suggest from the user's wardrobe unless explicitly asked otherwise. "
            f"Requested: {', '.join(categories)}."
        )
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": [
                {"type": "text", "text": transcript},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
            ]}
        ]
        for url in wardrobe_urls:
            messages[1]["content"].append({"type": "image_url", "image_url": {"url": url}})
        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            max_tokens=700
        )
        return response.choices[0].message.content
