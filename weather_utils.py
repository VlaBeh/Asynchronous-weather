import requests
from config import API_KEYS


def get_city_coordinates(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEYS}"
    response = requests.get(url)

    if response.status_code != 200:
        return None

    data = response.json()
    lat = data.get("coord", {}).get("lat")
    lon = data.get("coord", {}).get("lon")
    return (lat, lon) if lat and lon else None


def get_weather_by_coordinates(lat, lon):
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEYS}"
    response = requests.get(url)

    if response.status_code != 200:
        return None

    data = response.json()
    temp_kelvin = data.get("main", {}).get("temp")
    description = data.get("weather", [{}])[0].get("description", "")
    timezone = data.get("timezone", "")

    if temp_kelvin is not None:
        return {
            "temperature": round(temp_kelvin - 273.15, 1),
            "description": description,
            "region": determine_region_from_timezone(timezone)
        }
    return None


def determine_region_from_timezone(timezone):
    if -39600 <= timezone <= -10800:
        return "America"
    elif 0 <= timezone <= 14400:
        return "Europe"
    elif 18000 <= timezone <= 43200:
        return "Asia"
    return "Other"
