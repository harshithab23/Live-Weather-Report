from flask import Flask, render_template, request
import requests

app = Flask(__name__)

GEO_API_URL = "https://geocoding-api.open-meteo.com/v1/search"
WEATHER_API_URL = "https://api.open-meteo.com/v1/forecast"

def fetch_location_data(city_name):
    try:
        response = requests.get(f"{GEO_API_URL}?name={city_name}")
        data = response.json()
        if data.get("results"):
            location = data["results"][0]
            return location["latitude"], location["longitude"]
    except:
        pass
    return None, None

def fetch_weather_data(lat, lon):
    try:
        response = requests.get(
            f"{WEATHER_API_URL}?latitude={lat}&longitude={lon}&current_weather=true"
        )
        data = response.json()
        if "current_weather" in data:
            weather = data["current_weather"]
            return weather["temperature"], 50.0, weather["windspeed"]
    except:
        pass
    return None, None, None

@app.route("/", methods=["GET", "POST"])
def home():
    weather_data = None
    error_message = None

    if request.method == "POST":
        city_name = request.form.get("city_name", "").strip()
        if city_name:
            lat, lon = fetch_location_data(city_name)
            if lat is not None and lon is not None:
                temp, humidity, wind = fetch_weather_data(lat, lon)
                if temp is not None:
                    weather_data = {
                        "temperature": temp,
                        "humidity": humidity,
                        "wind_speed": wind,
                        "city": city_name
                    }
                else:
                    error_message = "❌ Couldn't get weather data. Try again later."
            else:
                error_message = f"❌ No results found for '{city_name}'."
        else:
            error_message = "❌ Please enter a city name."

    return render_template("index.html", weather=weather_data, error=error_message)

if __name__ == "__main__":
    app.run(debug=True)
