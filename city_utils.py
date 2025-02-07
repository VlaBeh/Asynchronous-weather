from fuzzywuzzy import process
from transliterate import translit
import requests
from config import API_KEYS


def load_cities(filename="cities.txt"):
    with open(filename, "r", encoding="utf-8") as file:
        return {line.strip().title() for line in file if line.strip()}


KNOWN_CITIES = load_cities()


def normalize_city(city):
    city = city.strip().title()
    match, score = process.extractOne(city, KNOWN_CITIES)
    return match if score > 80 else city


def transliterate_city(city):
    transliterated = translit(city, reversed=True)
    match, score = process.extractOne(transliterated, KNOWN_CITIES)
    return match if score > 80 else transliterated


def get_city_coordinates(city):
    """Отримання координат міста через API"""
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEYS}"
    response = requests.get(url)

    if response.status_code != 200:
        return None

    data = response.json()
    return {
        "lat": data.get("coord", {}).get("lat"),
        "lon": data.get("coord", {}).get("lon")
    }


def process_cities(cities):
    processed = []

    for city in cities:
        norm_city = normalize_city(city)
        if norm_city not in KNOWN_CITIES:
            norm_city = transliterate_city(city)

        coords = get_city_coordinates(norm_city)
        if coords:
            processed.append({"name": norm_city, "coordinates": coords})

    return processed


