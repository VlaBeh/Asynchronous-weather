from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from celery.result import AsyncResult
from app.tasks import process_weather_data
import redis

app = FastAPI()
redis_client = redis.Redis(host='localhost', port=6379, db=0)


class CitiesRequest(BaseModel):
    cities: list[str]


@app.post("/weather")
async def get_weather(request: CitiesRequest):
    task = process_weather_data.delay(request.cities)
    redis_client.set(task.id, "running")
    return {"task_id": task.id}


@app.get("/tasks/{task_id}")
async def get_task_status(task_id: str):
    task_result = AsyncResult(task_id)
    if task_result.state == "SUCCESS":
        return {"status": "completed", "result_url": f"/results/{task_id}"}
    elif task_result.state == "FAILURE":
        return {"status": "failed"}
    return {"status": task_result.state}
