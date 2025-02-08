from celery import Celery
from city_utils import process_cities
from weather_utils import get_weather_by_coordinates
import json
import os
from config import REDIS_BROKER, RESULT_BACKEND
from loguru import logger

celery_app = Celery("tasks", broker=REDIS_BROKER, backend=RESULT_BACKEND)

logger.add("weather_service.log", rotation="1 MB", level="INFO")


@celery_app.task
def process_weather_task(cities):
    """Асинхронна обробка міст"""
    results = {"Europe": [], "America": [], "Asia": []}

    for city in process_cities(cities):
        coords = city["coordinates"]
        weather = get_weather_by_coordinates(coords["lat"], coords["lon"])

        if weather:
            results[weather["region"]].append({
                "city": city["name"],
                "temperature": weather["temperature"],
                "description": weather["description"]
            })
        else:
            logger.warning(f"Не вдалося отримати погоду для {city['name']}")

    for region, data in results.items():
        if data:
            save_results(region, data)

    return results


def save_results(region, data):
    """Збереження результатів у JSON"""
    os.makedirs(f"weather_data/{region}", exist_ok=True)
    with open(f"weather_data/{region}/task_results.json", "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)
