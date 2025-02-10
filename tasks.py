import logging
from celery import Celery
from Utils.city_utils import process_cities
from Utils.weather_utils import get_weather_by_coordinates
import json
import os
from Settings.config import REDIS_BROKER, RESULT_BACKEND
from Settings.loger_config import logger

celery_app = Celery("tasks", broker=REDIS_BROKER, backend=RESULT_BACKEND)


@celery_app.task
def process_weather_task(cities):
    """Asynchronous processing of cities"""
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
            logger.warning(f"Couldn't get weather for city: {city['name']}")

    for region, data in results.items():
        if data:
            save_results(region, data)

    return results


def save_results(region, data):
    os.makedirs(f"weather_data/{region}", exist_ok=True)
    file_path = f"weather_data/{region}/task_results.json"

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)
        file.flush()

    logging.info(f"Saved new results to: {file_path}")

