import requests
import os
from dotenv import load_dotenv

load_dotenv()

FACE_API_KEY = os.getenv("FACE_API_KEY")
FACE_API_SECRET = os.getenv("FACE_API_SECRET")

def detect_face(image_path: str):
    url = "https://api-us.faceplusplus.com/facepp/v3/detect"
    image_file = open(image_path, "rb")
    files = {"image_file": image_file}
    data = {
        "api_key": FACE_API_KEY,
        "api_secret": FACE_API_SECRET,
        "return_attributes": "facequality"
    }

    response = requests.post(url, data=data, files=files)
    result = response.json()

    if "faces" in result and result["faces"]:
        return analyze_face(result["faces"][0]["face_token"])
    else:
        print("No face detected!")
        return None

def analyze_face(face_token: str):
    url = "https://api-us.faceplusplus.com/facepp/v3/face/analyze"
    
    data = {
        "api_key": FACE_API_KEY,
        "api_secret": FACE_API_SECRET,
        "face_tokens": face_token,
        "return_attributes": "age,gender,eyestatus,beauty,mouthstatus,skinstatus"
    }

    response = requests.post(url, data=data)
    result = response.json()
    print(result)
    return result

image_path = "/home/syeda/Smart-Mirror/dark.jpeg"
face_data = detect_face(image_path)

print(face_data)
