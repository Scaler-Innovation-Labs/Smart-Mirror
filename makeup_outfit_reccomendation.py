from google import genai
from google.genai import types
from dotenv import load_dotenv
import PIL.Image
import os
from weather import Weather
load_dotenv()

image: PIL.Image.Image = PIL.Image.open('/home/syeda/Smart-Mirror/test.jpeg')
#factors that are needed - weather, wadrobe, face attributes, occasion, time of the day
weather: str = Weather().get_coordinates()
wadrobe: set[str] = {
    'pink shirt',
    'black pants',
    'black shoes',
    'white skirt',
    'floral dress',
    'black dress',
}
client: genai.Client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents=[f"Suggest me one outfit and the makeup complimenting my outfit and face attributes from my {wadrobe}as i am going for a party during this weather {weather}", image])

print(response.text)