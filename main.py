from typing import List
from fastapi import FastAPI
from celery.result import AsyncResult
from pydantic import BaseModel
from tasks import process_weather_task
import json

app = FastAPI()


class WeatherRequest(BaseModel):
    cities: List[str]


@app.post("/weather/")
async def get_weather(request: WeatherRequest):
    task = process_weather_task.apply_async(args=[request.cities])
    return {"task_id": task.id}


@app.get("/tasks/{task_id}")
async def get_task_status(task_id: str):
    task_result = AsyncResult(task_id)
    if task_result.status == "SUCCESS" and task_result.result:
        filtered_result = {region: cities for region, cities in task_result.result.items() if cities}
        return {
            "task_id": task_id,
            "status": task_result.status,
            "result": filtered_result
        }
    return {"task_id": task_id, "status": task_result.status, "result": task_result.result}


@app.get("/results/{region}")
async def get_results(region: str):
    file_path = f"weather_data/{region}/task_results.json"
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return {"status": "completed", "results": json.load(file)}
    except FileNotFoundError:
        return {"status": "not_found", "message": "Дані не знайдені"}
