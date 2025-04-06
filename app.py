<<<<<<< HEAD
from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# API URLs
GEO_API_URL = "https://geocoding-api.open-meteo.com/v1/search"
WEATHER_API_URL = "https://api.open-meteo.com/v1/forecast"

# Function to fetch location coordinates
def fetch_location_data(city_name):
    try:
        url = f"{GEO_API_URL}?name={city_name}"
        response = requests.get(url)
        data = response.json()

        if "results" in data and len(data["results"]) > 0:
            location = data["results"][0]
            return location["latitude"], location["longitude"]
        else:
            return None, None
    except:
        return None, None

# Function to fetch weather data
def fetch_weather_data(latitude, longitude):
    try:
        url = f"{WEATHER_API_URL}?latitude={latitude}&longitude={longitude}&current_weather=true"
        response = requests.get(url)
        data = response.json()

        if "current_weather" in data:
            weather = data["current_weather"]
            return weather["temperature"], 50.0, weather["windspeed"]  # Simulated Humidity
        else:
            return None, None, None
    except:
        return None, None, None

@app.route("/", methods=["GET", "POST"])
def home():
    weather_data = None
    if request.method == "POST":
        city_name = request.form.get("city_name", "").strip()
        if city_name:
            latitude, longitude = fetch_location_data(city_name)
            if latitude is not None and longitude is not None:
                temperature, humidity, wind_speed = fetch_weather_data(latitude, longitude)
                if temperature is not None:
                    weather_data = {
                        "temperature": temperature,
                        "humidity": humidity,
                        "wind_speed": wind_speed,
                        "city": city_name
                    }
    return render_template("index.html", weather=weather_data)

if __name__ == "__main__":
    app.run(debug=True)
=======
from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# API URLs
GEO_API_URL = "https://geocoding-api.open-meteo.com/v1/search"
WEATHER_API_URL = "https://api.open-meteo.com/v1/forecast"

# Function to fetch location coordinates
def fetch_location_data(city_name):
    try:
        url = f"{GEO_API_URL}?name={city_name}"
        response = requests.get(url)
        data = response.json()

        if "results" in data and len(data["results"]) > 0:
            location = data["results"][0]
            return location["latitude"], location["longitude"]
        else:
            return None, None
    except:
        return None, None

# Function to fetch weather data
def fetch_weather_data(latitude, longitude):
    try:
        url = f"{WEATHER_API_URL}?latitude={latitude}&longitude={longitude}&current_weather=true"
        response = requests.get(url)
        data = response.json()

        if "current_weather" in data:
            weather = data["current_weather"]
            return weather["temperature"], 50.0, weather["windspeed"]  # Simulated Humidity
        else:
            return None, None, None
    except:
        return None, None, None

@app.route("/", methods=["GET", "POST"])
def home():
    weather_data = None
    if request.method == "POST":
        city_name = request.form.get("city_name", "").strip()
        if city_name:
            latitude, longitude = fetch_location_data(city_name)
            if latitude is not None and longitude is not None:
                temperature, humidity, wind_speed = fetch_weather_data(latitude, longitude)
                if temperature is not None:
                    weather_data = {
                        "temperature": temperature,
                        "humidity": humidity,
                        "wind_speed": wind_speed,
                        "city": city_name
                    }
    return render_template("index.html", weather=weather_data)

if __name__ == "__main__":
    app.run(debug=True)
>>>>>>> 83dc0e6ef85d832189c310ba8d7fdae1c4c45a86
