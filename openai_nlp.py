import os
import base64
import json
import re
import requests
import logging
from dotenv import load_dotenv
import openai

load_dotenv()
logger = logging.getLogger(__name__)

class NLPProcessor:
    def __init__(self):
        """Initializes the NLP processor with OpenAI client and conversation history."""
        self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.conversation_history = []
        self.fastapi_url = os.getenv("FASTAPI_URL", "http://127.0.0.1:8000")


    def encode_image(self, image_path):
        """Encodes an image file to a base64 string."""
        with open(image_path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")

    def detect_intent(self, prompt):
        """Uses GPT-4o to classify the user's intent."""
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "Classify the user's request into one of the following categories: 'outfit', 'makeup', 'jewelry', or 'general'."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0,
                max_tokens=20
            )
            return response.choices[0].message.content.lower().strip().replace("\"", "")
        except openai.APIError as e:
            logger.error(f"OpenAI API Error in intent detection: {e}")
            return "general"

    def fetch_wardrobe_items(self):
        """Fetches all wardrobe item URLs from the FastAPI backend."""
        try:
            # First, get all categories
            response = requests.get(f"{self.fastapi_url}/wardrobe", timeout=10)
            response.raise_for_status()
            categories = response.json()
            
            all_urls = []
            # Then, get items for each category
            for category_info in categories:
                category_name = category_info["name"].strip()
                items_response = requests.get(f"{self.fastapi_url}/wardrobe/{category_name}", timeout=10)
                items_response.raise_for_status()
                all_urls.extend([item["image_url"].strip() for item in items_response.json() if item.get("image_url", "").startswith("http")])
            
            logger.info(f"Fetched {len(all_urls)} items from wardrobe.")
            return all_urls
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to fetch wardrobe items from FastAPI: {e}")
            return None

    def analyze_user_image(self, image_path):
        """Analyzes the user's image to determine gender, skin tone, and hair texture."""
        base64_image = self.encode_image(image_path)
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a stylist AI. Analyze the person in the image. "
                            "Return a single, minified JSON object with three keys: "
                            "'gender' (string: 'male', 'female', or 'unisex'), "
                            "'skin_tone' (string: 'fair', 'light', 'medium', 'tan', 'deep'), and "
                            "'hair_texture' (string: 'straight', 'wavy', 'curly', 'coily')."
                        )
                    },
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": "Analyze the person in this image and provide the JSON output."},
                            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                        ]
                    }
                ],
                max_tokens=200
            )
            raw = response.choices[0].message.content.strip()
            if raw.startswith("```json"):
                raw = raw[7:-3].strip()
            return json.loads(raw)
        except (json.JSONDecodeError, openai.APIError) as e:
            logger.error(f"Image analysis failed: {e}")
            return {"gender": "unknown", "skin_tone": "unknown", "hair_texture": "unknown"}

    def generate_general_response(self, prompt):
        """Generates a response for a general, non-fashion-related query."""
        # A simple pass-through for now, can be expanded later
        return self.generate_fashion_response(prompt, None, [], "general", {})

    def generate_fashion_response(self, transcript, image_path, wardrobe_urls, requested_categories, user_analysis):
        """Generates a detailed fashion response based on all available context."""
        user_gender = user_analysis.get("gender", "unknown")

        system_prompt = (
            "You are an expert AI Fashion Stylist named 'Mirror'. Your tone is professional, friendly, and helpful. "
            "You must follow these rules precisely:\n"
            "1. **Analyze and Verify:** The user in the image has been identified as '{user_gender}'. First, analyze the clothing items in the provided wardrobe URLs to determine their intended gender (e.g., womenswear, menswear).\n"
            "2. **Handle Mismatch Professionally:** If the user's gender does NOT align with the wardrobe's gender (e.g., a male user with a womenswear wardrobe), you MUST NOT suggest any items. Instead, respond politely and professionally. For example: 'It appears my current wardrobe is tailored for womenswear, so I don't have the right selections for you at the moment. However, I can still offer general style advice if you'd like!'\n"
            "3. **Strict Wardrobe Adherence:** If the genders align, all your outfit suggestions MUST exclusively use items from the provided wardrobe URLs. Do not invent items.\n"
            "4. **Handle No Suitable Items:** If you cannot create a suitable, complete outfit from the available wardrobe that matches the user's request, clearly state that you couldn't find a perfect match in the current wardrobe.\n"
            "5. **Provide Purchase Suggestions:** After stating you couldn't find a match (as per rule #4), pivot to providing actionable shopping advice. Suggest 1-2 specific items the user could purchase to enhance their wardrobe. For example: 'To complete a look like this, a pair of dark-wash slim-fit jeans would be a fantastic and versatile addition to your collection.'\n"
            "6. **Be Conversational:** If a user's request is vague (e.g., 'what should I wear?'), ask clarifying questions (e.g., 'What's the occasion? Are you going for a casual or formal look?')."
        ).format(user_gender=user_gender)

        # Trim conversation history to keep it manageable
        self.conversation_history = self.conversation_history[-6:]
        
        messages = [{"role": "system", "content": system_prompt}] + self.conversation_history

        user_message_content = [{"type": "text", "text": transcript}]
        if image_path:
            base64_image = self.encode_image(image_path)
            user_message_content.append({"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}})
        for url in wardrobe_urls:
            user_message_content.append({"type": "image_url", "image_url": {"url": url}})

        messages.append({"role": "user", "content": user_message_content})

        try:
            response = self.client.chat.completions.create(model="gpt-4o", messages=messages, max_tokens=1000)
            assistant_response = response.choices[0].message.content
            self.conversation_history.append({"role": "user", "content": transcript})
            self.conversation_history.append({"role": "assistant", "content": assistant_response})
            return assistant_response
        except openai.APIError as e:
            logger.error(f"OpenAI fashion response generation failed: {e}")
            return "I'm sorry, I encountered an issue while trying to come up with a suggestion."