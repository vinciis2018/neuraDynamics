import os
import requests
from langchain_core.tools import tool

@tool
def get_weather(city: str) -> str:
    """
    Fetches the current weather for a given city using OpenWeatherMap API.
    Args:
        city (str): The name of the city to fetcn weather for.
    Returns:
        str: A string containing weather details or an error message.
    """
    api_key = os.getenv("OPENWEATHERMAP_API_KEY") or "c783f21ad2b6be85e380e77cdbe37e22"
    if not api_key:
        return "Error: OpenWeatherMap API key is missing."

    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric"
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()
        
        weather_desc = data['weather'][0]['description']
        temp = data['main']['temp']
        feels_like = data['main']['feels_like']
        humidity = data['main']['humidity']
        
        return (f"The weather in {city} is currently {weather_desc} with a temperature of {temp}°C "
                f"(feels like {feels_like}°C) and humdity of {humidity}%.")
    except requests.exceptions.HTTPError as http_err:
        return f"HTTP error occurred: {http_err}"
    except Exception as err:
        return f"An error occurred: {err}"
