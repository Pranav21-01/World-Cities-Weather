import requests
import pandas as pd
import matplotlib.pyplot as plt
import json


try:
    with open("config.json", "r") as file:
        config = json.load(file)
        GOOGLE_API_KEY = config["GOOGLE_API_KEY"]
        OPENWEATHER_API_KEY = config["OPENWEATHER_API_KEY"]
except FileNotFoundError:
    print("Error: 'config.json' file not found. Please create it based on 'config.json.example'.")
    exit()

#
GEOCODING_URL = "https://maps.googleapis.com/maps/api/geocode/json"
ONECALL_URL = "https://api.openweathermap.org/data/3.0/onecall"

def get_city_coordinates_google(city):
    params = {"address": city, "key": GOOGLE_API_KEY}
    response = requests.get(GEOCODING_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        if "results" in data and data["results"]:
            location = data["results"][0]["geometry"]["location"]
            return location["lat"], location["lng"]
        else:
            print(f"City not found: {city}")
    return None, None

def get_weather_data(lat, lon):
    params = {
        "lat": lat, "lon": lon,
        "exclude": "minutely,hourly",
        "units": "metric",
        "appid": OPENWEATHER_API_KEY
    }
    response = requests.get(ONECALL_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        return {
            "Temperature": data["current"]["temp"],
            "Weather": data["current"]["weather"][0]["description"],
            "Humidity": data["current"]["humidity"]
        }
    print(f"Error fetching weather data: {response.status_code}")
    return None

def main():
    cities = ["New York", "London", "Sydney", "Paris", "Mumbai", "Munich"]
    weather_data = []

    for city in cities:
        lat, lon = get_city_coordinates_google(city)
        if lat and lon:
            weather = get_weather_data(lat, lon)
            if weather:
                weather["City"] = city
                weather_data.append(weather)

    df = pd.DataFrame(weather_data)
    print(df)

    plt.figure(figsize=(10, 6))
    bars = plt.bar(df["City"], df["Temperature"], color="skyblue", edgecolor="black")

    max_temp_city = df.loc[df["Temperature"].idxmax()]
    min_temp_city = df.loc[df["Temperature"].idxmin()]

    for bar, temp in zip(bars, df["Temperature"]):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), f"{temp}°C", ha="center", va="bottom")

    bars[df["Temperature"].idxmax()].set_color("red")
    bars[df["Temperature"].idxmin()].set_color("green")

    plt.title("City Temperatures")
    plt.xlabel("City")
    plt.ylabel("Temperature (°C)")
    plt.xticks(fontsize=14)
    plt.show()

    print(f"Highest temperature: {max_temp_city['City']} ({max_temp_city['Temperature']}°C)")
    print(f"Lowest temperature: {min_temp_city['City']} ({min_temp_city['Temperature']}°C)")

if __name__ == "__main__":
    main()
