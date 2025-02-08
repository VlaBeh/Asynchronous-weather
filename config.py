import os

API_KEYS = "b64ec4a3fab3ca0b27569f57f625d646"
BASE_API_URL = "https://api.weatherapi.com/v1/current.json"
REDIS_BROKER = os.getenv("REDIS_BROKER", "redis://redis:6379/0")
RESULT_BACKEND = os.getenv("RESULT_BACKEND", "redis://redis:6379/1")
CELERY_BROKER_URL = "redis://redis:6379/0"

LOG_FILE = "weather_service.log"
