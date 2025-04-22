import base64
import json
import requests
from datetime import datetime

data_store_file = "metadata_store.json"
OPENAI_API_KEY = "your_openai_api_key"  # Replace with your OpenAI API key
OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"

def load_data_store():
    """Loads stored metadata from a JSON file."""
    try:
        with open(data_store_file, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_data_store(data_store):
    """Saves metadata to a JSON file."""
    with open(data_store_file, "w") as file:
        json.dump(data_store, file, indent=4)

def encode_image(image_path):
    """Encodes an image to base64 format."""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

def generate_metadata(image_path, user_id, image_url):
    """Sends an image to the OpenAI API to generate metadata dynamically."""
    image_base64 = encode_image(image_path)

    # Prepare prompt for ChatGPT
    prompt = f"""
    Describe the clothing item in this image with details like category, color, pattern, fabric, season, formality, and weather suitability.
    (Note: The image provided is a base64 encoded representation of the clothing item)
    """

    payload = {
        "model": "gpt-4",  # You can use other models such as "gpt-3.5-turbo"
        "messages": [
            {"role": "system", "content": "You are a helpful assistant that describes clothing items."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,  # Control the creativity of the response
        "max_tokens": 150
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}"
    }

    # Send the prompt to OpenAI API
    response = requests.post(OPENAI_API_URL, headers=headers, json=payload)

    if response.status_code == 200:
        # Extract the descriptive text from the response
        metadata_text = response.json()["choices"][0]["message"]["content"]
        print("Description received from ChatGPT API:")
        print(metadata_text)

        # Now, generate a vector embedding for the description
        embedding_payload = {
            "model": "text-embedding-ada-002",  # Use an embedding model
            "input": metadata_text
        }

        # Send description for embedding generation
        embedding_response = requests.post("https://api.openai.com/v1/embeddings", headers=headers, json=embedding_payload)

        if embedding_response.status_code == 200:
            # Extract the vector embedding from the response
            vector_embedding = embedding_response.json()["data"][0]["embedding"]
            print("Generated Vector Embedding:")
            print(vector_embedding)
            metadata = {
                "description": metadata_text,
                "vector_embedding": vector_embedding
            }
        else:
            print("Error generating vector embedding:", embedding_response.text)
            metadata = {"description": metadata_text, "vector_embedding": None}
        
        # Save metadata to the data store
        data_store = load_data_store()
        data_store[metadata["description"]] = metadata
        save_data_store(data_store)

        return metadata
    else:
        print("Error fetching metadata:", response.text)
        return None

# Run the Script
if __name__ == "__main__":
    image_path = "Final/Screenshot 2025-03-31 211106.png"  # Replace with actual image path
    user_id = "user_67890"
    image_url = "https://your-storage.com/user123/shirt1.jpg"
    
    metadata = generate_metadata(image_path, user_id, image_url)
    if metadata:
        print("Generated Metadata:")
        print(json.dumps(metadata, indent=4))
