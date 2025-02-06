import os
from dotenv import load_dotenv
load_dotenv()

API_KEYS = os.getenv("OPENWEATHER_API_KEYS").split(",")
REDIS_URL = "redis://localhost:6379"
WEATHER_API_URL = "https://api.openweathermap.org/data/2.5/weather?q={}&appid={}"
