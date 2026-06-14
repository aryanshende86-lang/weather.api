import os
import json
import requests
import os
from dotenv import load_dotenv  
load_dotenv() 

API_KEY = os.getenv("OPENWEATHER_API_KEY")
WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"
AIR_URL = "https://api.openweathermap.org/data/2.5/air_pollution"
HISTORY_FILE = "history.json"


def load_history():
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as file:
                return json.load(file)
        except:
            return []
    return []


def save_history(history):
    with open(HISTORY_FILE, "w", encoding="utf-8") as file:
        json.dump(history[:5], file, indent=2)


def aqi_text(aqi):
    if aqi == 1:
        return "Good"
    elif aqi == 2:
        return "Fair"
    elif aqi == 3:
        return "Moderate"
    elif aqi == 4:
        return "Poor"
    elif aqi == 5:
        return "Very Poor"
    else:
        return "Unknown"


def aqi_advice(aqi):
    if aqi == 1:
        return "Air quality is good. You can go outside normally."
    elif aqi == 2:
        return "Air quality is fair. Most people are fine outside."
    elif aqi == 3:
        return "Sensitive people should reduce outdoor activity."
    elif aqi == 4:
        return "Try to avoid long outdoor exposure."
    elif aqi == 5:
        return "Avoid going outside if possible."
    else:
        return "No advisory available."


def get_weather(city):
    global API_KEY
    try:
        params = {
            "q" : city,
            "appid": API_KEY,
            "units" : "metric"
            
        }

        response = requests.get(WEATHER_URL, params=params, timeout=10)

        if response.status_code == 404:
            print("City not found. Please check the spelling and try again.")
            return None

        response.raise_for_status()
        data = response.json()

        lat = data["coord"]["lat"]
        lon = data["coord"]["lon"]

        return {
            "city": data["name"],
            "temp": round(data["main"]["temp"]),
            "feels_like": round(data["main"]["feels_like"]),
            "humidity": data["main"]["humidity"],
            "wind_speed": round(data["wind"]["speed"] * 3.6, 1),
            "condition": data["weather"][0]["description"].title(),
            "lat": lat,
            "lon": lon
        }

    except requests.exceptions.RequestException:
        print("Network error. Please check your internet connection.")
    except KeyError:
        print("Unexpected data format received from weather API.")

    return None


def get_aqi(lat, lon):
    global API_KEY
    try:
        params = {
            "lat" : lat,
            "lon" : lon,
            "appid": API_KEY
        }

        response = requests.get(AIR_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        return data["list"][0]["main"]["aqi"]

    except requests.exceptions.RequestException:
        print("Could not fetch AQI data.")
    except:
        print("Unexpected data format received from AQI API.")

    return None


def show_weather(info, aqi):
    print(f"\nWeather in {info['city']}")
    print(f"Temperature : {info['temp']}°C (Feels like {info['feels_like']}°C)")
    print(f"Humidity : {info['humidity']}%")
    print(f"Wind Speed : {info['wind_speed']} km/h")
    print(f"Condition : {info['condition']}")

    if aqi is not None:
        print(f"Air Quality Index: {aqi} — {aqi_text(aqi)}")
        print(f"Advisory: {aqi_advice(aqi)}")
    else:
        print("Air Quality Index: Not available")


def show_history(history):
    if not history:
        print("No history found.")
        return

    print("\nSearch History:")
    for item in history:
        print(f"\nCity: {item['city']}")
        print(f"Temperature: {item['temp']}°C")
        print(f"Feels like: {item['feels_like']}°C")
        print(f"Humidity: {item['humidity']}%")
        print(f"Wind Speed: {item['wind_speed']} km/h")
        print(f"Condition: {item['condition']}")
        print(f"AQI: {item.get('aqi', 'N/A')} ({item.get('aqi_label', 'Unknown')})")
        print(f"Advisory: {item.get('aqi_advice', 'Not available')}")


def main():
    if not API_KEY:
        print("API key not found. Please set OPENWEATHER_API_KEY in your environment.")
        return

    history = load_history()

    if history:
        last = history[0]
        print(f"Last search: {last['city']} - {last['temp']}°C, {last['condition']}")
    else:
        print("No previous search history.")

    while True:
        city = input("\nEnter city name (or type 'history' or 'exit'): ").strip()

        if city.lower() == "exit":
            print("Goodbye!")
            break

        if city.lower() == "history":
            show_history(history)
            continue

        if not city:
            print("Please enter a valid city name.")
            continue

        weather = get_weather(city)

        if weather:
            aqi = get_aqi(weather["lat"], weather["lon"])

            weather["aqi"] = aqi
            weather["aqi_label"] = aqi_text(aqi)
            weather["aqi_advice"] = aqi_advice(aqi)

            show_weather(weather, aqi)

            history.insert(0, weather)
            history = history[:5]
            save_history(history)


if __name__ == "__main__":
    main()
  
