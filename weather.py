import geocoder
from typing import Any
import os
import requests
from dotenv import load_dotenv
from requests.models import Response

load_dotenv()
WEATHER_API_KEY: str = os.getenv("WEATHER_API_KEY")

def get_coordinates() -> None:
    g: Any = geocoder.ip('me')
    lat: float = g.latlng[0]
    lon: float = g.latlng[1]
    print(lat, lon)
    get_weather(lat, lon)

def get_weather(lat: float, lon: float) -> Any:
    url: str = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={WEATHER_API_KEY}"
    response: Response = requests.get(url)
    data: Any = response.json()
    # print(data)
    return data

get_coordinates()

