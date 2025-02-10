import geocoder
from typing import Any
import os
import requests
from dotenv import load_dotenv
from requests.models import Response

load_dotenv()
WEATHER_API_KEY: str = os.getenv("WEATHER_API_KEY")

class Weather:
    def __init__(self)-> None:
        self.api_key: str = WEATHER_API_KEY

    def get_coordinates(self) -> None:
        g: Any = geocoder.ip('me')
        lat: float = g.latlng[0]
        lon: float = g.latlng[1]
        print(lat, lon)
        self.get_weather(lat, lon)

    def get_weather(self, lat: float, lon: float) -> Any:
        url: str = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={self.api_key}"
        response: Response = requests.get(url)
        data: Any = response.json()
        # print(data)
        return data

weather = Weather()
weather.get_coordinates()

