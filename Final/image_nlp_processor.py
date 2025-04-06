import openai
import os
from dotenv import load_dotenv
from openai import OpenAIError
import base64

class ImageNLPProcessor:
    def __init__(self):
        load_dotenv()
        self.OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

        if not self.OPENAI_API_KEY:
            raise ValueError("Missing OpenAI API Key. Set it in .env file.")

        self.client = openai.OpenAI(api_key=self.OPENAI_API_KEY)

    def encode_image(self, image_path):
        """Convert image to base64 for OpenAI vision model."""
        try:
            with open(image_path, "rb") as img_file:
                return base64.b64encode(img_file.read()).decode("utf-8")
        except FileNotFoundError:
            raise ValueError(f"Image file not found: {image_path}")

    def generate_response(self, text_input, image_path):
        """Send text and image to OpenAI and return response."""
        try:
            base64_image = self.encode_image(image_path)

            response = self.client.chat.completions.create(
                model="gpt-4-vision-preview",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": text_input},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=1000
            )

            return response.choices[0].message.content

        except OpenAIError as e:
            return f"⚠️ OpenAI API Error: {e}"
        except Exception as e:
            return f"⚠️ Unexpected Error: {e}"