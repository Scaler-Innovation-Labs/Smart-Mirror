import os
import base64
import requests
import json
import re
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

        # Initialize conversation history for adaptive responses
        self.conversation_history = []

    def encode_image(self, image_path):
        """Encodes the image as base64 for API processing."""
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")

    def detect_intent(self, prompt):
        """Detects if the request is about outfit, makeup, jewelry, or general query."""
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
        """Fetches wardrobe items from backend API."""
        FASTAPI_URL = "http://192.168.13.212:8000"
        try:
            response = requests.get(f"{FASTAPI_URL}/wardrobe")
            response.raise_for_status()
            categories = response.json()
            urls = []
            for c in categories:
                cat = c["name"].strip()
                r = requests.get(f"{FASTAPI_URL}/wardrobe/{cat}")
                r.raise_for_status()
                urls.extend([
                    item["image_url"].strip()
                    for item in r.json()
                    if item.get("image_url", "").startswith("http")
                ])
            return urls
        except requests.exceptions.RequestException:
            return None

    def analyze_user_image(self, image_path):
        """Analyzes user's image for skin tone and hair texture."""
        base64_image = self.encode_image(image_path)
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a professional stylist AI. "
                            "Analyze the person in the image only. "
                            "Return a strict JSON object with these keys:\n"
                            "- skin_tone: ['fair', 'light', 'medium', 'tan', 'deep']\n"
                            "- hair_texture: ['straight', 'wavy', 'curly', 'coily']\n"
                            "No explanations. JSON only."
                        )
                    },
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": "Analyze this image and return JSON only."},
                            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                        ]
                    }
                ],
                max_tokens=200
            )

            raw_output = response.choices[0].message.content.strip()
            try:
                return json.loads(raw_output)
            except json.JSONDecodeError:
                match = re.search(r'\{.*\}', raw_output, re.DOTALL)
                return json.loads(match.group(0)) if match else {"skin_tone": "unknown", "hair_texture": "unknown"}

        except Exception as e:
            print(f"Error analyzing image: {e}")
            return {"skin_tone": "unknown", "hair_texture": "unknown"}
    def generate_response(self, prompt): 
        try: 
            response = self.client.chat.completions.create( model="gpt-4", messages=[ {"role": "system", "content": "You are a professional fashion assistant."}, {"role": "user", "content": prompt} ], max_tokens=500 ) 
            return response.choices[0].message.content 
        except OpenAIError: 
            return "I had an issue processing your request."
    def generate_fashion_response(self, transcript, image_path, wardrobe_urls, requested_categories):
        """Conversational, adaptive fashion assistant."""
        base64_image = self.encode_image(image_path)

        category_map = {
            "outfit": "suggest clothing combinations",
            "jewelry": "suggest accessories that match",
            "makeup": "suggest makeup styles"
        }
        categories = [category_map[c] for c in requested_categories.split(",") if c in category_map]

        system_prompt = (
            "You are an expert AI Fashion Stylist and Outfit Matcher. "
            "Act as a friendly, conversational assistant. "
            "Steps to follow:\n"
            "1. Identify the user's needs by asking clarifying questions (event type, vibe, weather, color preferences).\n"
            "2. Analyze their inputs and wardrobe.\n"
            "3. Suggest 2-3 cohesive outfit combinations with brief explanations.\n"
            "4. Suggest optional accessories and style upgrades.\n"
        
            "- Do not repeat combinations unless asked.\n"
            "- Only suggest from available wardrobe images.\n"
            "- Keep language natural and non-repetitive.\n"
            "Output:\n"
            "1. Suggested Outfit Combinations\n"
            "2. Optional Style Upgrades\n"
            f"Requested: {', '.join(categories)}."
        )

        messages = [{"role": "system", "content": system_prompt}]
        messages += self.conversation_history

        user_message = {
            "role": "user",
            "content": [
                {"type": "text", "text": transcript},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
            ]
        }

        for url in wardrobe_urls:
            user_message["content"].append({"type": "image_url", "image_url": {"url": url}})

        messages.append(user_message)

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                max_tokens=1000
            )

            # Update memory for adaptive interaction
            self.conversation_history.append({"role": "user", "content": transcript})
            self.conversation_history.append(
                {"role": "assistant", "content": response.choices[0].message.content}
            )

            return response.choices[0].message.content
        except OpenAIError as e:
            return f"I encountered an issue: {e}"
