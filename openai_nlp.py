import os
import base64
import json
import re
import requests
from dotenv import load_dotenv
import openai
from openai import OpenAIError

class NLPProcessor:
    def __init__(self):
        load_dotenv()
        self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.conversation_history = []

    def encode_image(self, image_path):
        with open(image_path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")

    def detect_intent(self, prompt):
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "Classify: outfit, makeup, jewelry, or general."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0,
                max_tokens=20
            )
            return response.choices[0].message.content.lower().strip()
        except Exception:
            return "general"

    def fetch_wardrobe_items(self):
        FASTAPI_URL = "http://192.168.13.212:8000"
        try:
            response = requests.get(f"{FASTAPI_URL}/wardrobe")
            response.raise_for_status()
            urls = []
            for c in response.json():
                cat = c["name"].strip()
                r = requests.get(f"{FASTAPI_URL}/wardrobe/{cat}")
                r.raise_for_status()
                urls.extend([item["image_url"].strip()
                             for item in r.json()
                             if item.get("image_url", "").startswith("http")])
            return urls
        except requests.exceptions.RequestException:
            return None

    def analyze_user_image(self, image_path):
        base64_image = self.encode_image(image_path)
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a stylist AI. "
                            "Return JSON with: skin_tone ['fair','light','medium','tan','deep'], "
                            "hair_texture ['straight','wavy','curly','coily']."
                        )
                    },
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": "Analyze this image."},
                            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                        ]
                    }
                ],
                max_tokens=200
            )
            raw = response.choices[0].message.content.strip()
            try:
                return json.loads(raw)
            except json.JSONDecodeError:
                match = re.search(r'\{.*\}', raw, re.DOTALL)
                return json.loads(match.group(0)) if match else {"skin_tone": "unknown", "hair_texture": "unknown"}
        except Exception:
            return {"skin_tone": "unknown", "hair_texture": "unknown"}

    def generate_response(self, prompt):
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "system", "content": "You are a professional fashion assistant."},
                          {"role": "user", "content": prompt}],
                max_tokens=500
            )
            return response.choices[0].message.content
        except OpenAIError:
            return "I had an issue processing your request."

    def generate_fashion_response(self, transcript, image_path, wardrobe_urls, requested_categories):
        base64_image = self.encode_image(image_path)
        category_map = {
            "outfit": "clothing combinations",
            "jewelry": "matching accessories",
            "makeup": "makeup looks"
        }
        categories = [category_map[c] for c in requested_categories.split(",") if c in category_map]

        system_prompt = (
            "You are an expert AI Fashion Stylist. "
            "Act as a friendly, conversational assistant. "
            "If the request is vague (e.g., 'I need an outfit'), ask clarifying questions "
            "like event type, theme, weather, or vibe before suggesting. "
            "Once clarified, suggest 2–3 cohesive outfits with explanations. "
            "Also suggest optional style upgrades. "
            "Use wardrobe images provided. "
            f"Focus on: {', '.join(categories)}."
        )

        messages = [{"role": "system", "content": system_prompt}] + self.conversation_history

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
            response = self.client.chat.completions.create(model="gpt-4o", messages=messages, max_tokens=1000)
            self.conversation_history.append({"role": "user", "content": transcript})
            self.conversation_history.append({"role": "assistant", "content": response.choices[0].message.content})
            return response.choices[0].message.content
        except OpenAIError as e:
            return f"I encountered an issue: {e}"
