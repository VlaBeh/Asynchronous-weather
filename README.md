# Asynchronous-weather

## How to Run the Project

#### Prerequisites

Ensure you have the following installed:
Docker and Docker Compose
Python 3.9+ (for local execution without Docker)

#### Running with Docker

Clone the repository:
git clone https://github.com/VlaBeh/Asynchronous-weather.git
cd weatherProject

Start the services using Docker Compose:
docker-compose up --build

This command will start:
FastAPI (API service on port 8000)
Redis (message broker on port 6379)
Celery (background task processor)

Verify the setup:
FastAPI should be available at: http://localhost:8000/docs
Running Without Docker (Local Development)

Install dependencies:
pip install -r requirements.txt
Start Redis manually (if not using Docker).

Run FastAPI:
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

Start Celery worker:
celery -A tasks worker --loglevel=info

### API Endpoints

#### How to get an "OPENWEATHER_API_KEYS":

1. Go to https://openweathermap.org/
2. Create an account by providing your email, username, and password
3. Navigate to the API keys section https://home.openweathermap.org/api_keys
4. Put your API_Key to .env

#### Common errors:

"PENDING" - mostly because API can share only 60 city names per minute

#### Submit a Weather Data Processing Task

Method: POST
URL: /weather/

Request Body (JSON):
{
  "cities": ["London", "New York", "Tokyo"]
}
Response:
{
  "task_id": "12345678-abcd-90ef-ghij-1234567890kl"
}

Description:
Submits a list of city names for processing.
The system normalizes city names, retrieves coordinates, and fetches weather data asynchronously.
Returns a task ID to track the progress.

#### Check Task Status

Method: GET
URL: /tasks/{task_id}

**Example:** /tasks/12345678-abcd-90ef-ghij-1234567890kl

Response (if completed):
{
  "task_id": "12345678-abcd-90ef-ghij-1234567890kl",
  "status": "SUCCESS",
  "result": {
    "Europe": [
      {"city": "London", "temperature": 12.3, "description": "clear sky"},
      {"city": "Paris", "temperature": 8.5, "description": "rain"}
    ],
    "America": [
      {"city": "New York", "temperature": 10.1, "description": "cloudy"}
    ],
    "Asia": [
      {"city": "Tokyo", "temperature": 15.4, "description": "sunny"}
    ]
  }
}

Description:
Retrieves the task status and processed weather data (if available).
Returns "PENDING", "PROCESSING", or "SUCCESS".
If successful, returns weather details grouped by region.

#### Retrieve Weather Data by Region

Method: GET
URL: /results/{region}

**Example:** /results/Europe

Response:
{
  "status": "completed",
  "results": [
    {"city": "London", "temperature": 12.3, "description": "clear sky"},
    {"city": "Paris", "temperature": 8.5, "description": "rain"}
  ]
}
Description:
Fetches the latest processed weather data for a specific region (Europe, America, Asia).
Returns a "not_found" status if no data is available. 

### Technical Details

#### Core Features

Asynchronous Task Processing: Uses Celery to handle weather data requests in the background.

City Name Normalization: Supports different spellings and non-Latin city names.

Weather Data Retrieval: Fetches weather information from an external API using city coordinates.

Data Storage & Organization: Saves results in JSON files grouped by region (weather_data/Europe/, etc.).

Error Handling & Logging:
If a city is invalid or API calls fail, errors are logged.

Uses loguru and standard logging for debugging.