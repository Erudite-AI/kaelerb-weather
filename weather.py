from dotenv import load_dotenv
from pprint import pprint
import requests
from datetime import datetime
import os

load_dotenv()


def get_current_weather(city="Lagos"):
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {                                  # FIXED 1: requests builds a safe URL for us
        "appid": os.getenv("API_KEY"),
        "q": city,
        "units": "metric",
    }

    try:
            response = requests.get(url, params=params, timeout=10)   # FIXED 2: stop waiting after 10s
            return response.json()
    except requests.exceptions.RequestException as e:                  # FIXED 3: internet problems
        print("Weather request failed:", e)
        return None
    
def get_local_time(lat, lon):
    url = "http://api.timezonedb.com/v2.1/get-time-zone"
    params = {
        "key": os.getenv("TIMEZONE_API_KEY"),
        "format": "json",
        "by": "position",
        "lat": lat,
        "lng": lon,
    }

    try:
        data = requests.get(url, params=params, timeout=10).json()   # FIXED 2: stop waiting after 10s
    except requests.exceptions.RequestException as e: 
        print("Local time request failed:", e)
        return None                 # FIXED 3: internet problems

    if data.get("status") != "OK":
        return None

    local = datetime.strptime(data["formatted"], "%Y-%m-%d %H:%M:%S")
    return local.strftime("%A, %d %B %Y, %I:%M %p")
    
    
if __name__ == "__main__":
    print('\n*** Get Current Weather Condition ***')

    city = input("\nPlease enter a city name: ")

    weather_data = get_current_weather(city)

    print("\n")
    pprint(weather_data)