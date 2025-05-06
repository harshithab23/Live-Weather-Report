from flask import Flask, render_template, request
import requests

app = Flask(__name__)

GEO_API_URL = "https://geocoding-api.open-meteo.com/v1/search"
WEATHER_API_URL = "https://api.open-meteo.com/v1/forecast"

# Fetch location data (latitude, longitude) based on city name
def fetch_location_data(city_name):
    try:
        response = requests.get(f"{GEO_API_URL}?name={city_name}")
        data = response.json()
        if data.get("results"):
            location = data["results"][0]
            return location["latitude"], location["longitude"]
    except Exception as e:
        print(f"Error fetching location data: {e}")
    return None, None

# Fetch weather data based on latitude and longitude
def fetch_weather_data(lat, lon):
    try:
        response = requests.get(
            f"{WEATHER_API_URL}?latitude={lat}&longitude={lon}"
            "&daily=temperature_2m_max,temperature_2m_min,relative_humidity_2m_max,windspeed_10m_max"
            "&current_weather=true"
            "&timezone=auto"
        )
        data = response.json()

        # Debugging: Print the response data
        print(data)

        forecast = []
        current = {}

        if "daily" in data:
            daily = data["daily"]
            for i in range(len(daily["time"])):
                forecast.append({
                    "date": daily["time"][i],
                    "temp_max": daily["temperature_2m_max"][i],
                    "temp_min": daily["temperature_2m_min"][i],
                    "humidity": daily["relative_humidity_2m_max"][i],
                    "wind_speed": daily["windspeed_10m_max"][i]
                })

        # Current weather data
        current_data = data.get("current_weather", {})
        current = {
            "temperature": current_data.get("temperature", "N/A"),
            "windspeed": current_data.get("windspeed", "N/A"),
            "weathercode": current_data.get("weathercode", None)
        }

        # Determine condition based on weather code
        rain_codes = [51, 53, 55, 61, 63, 65, 80, 81, 82]
        if current["weathercode"] in rain_codes:
            condition = "rainy"
        else:
            first_temp = forecast[0]["temp_max"] if forecast else 0
            if first_temp > 20:
                condition = "sunny"
            elif first_temp >= 7:
                condition = "normal"
            else:
                condition = "cold"

        return forecast, condition, current

    except Exception as e:
        print(f"Error fetching weather data: {e}")
    return None, "default", {}

@app.route("/", methods=["GET", "POST"])
def home():
    forecast_data = None
    current_data = {}
    error_message = None
    condition = "default"
    city_name = ""

    if request.method == "POST":
        city_name = request.form.get("city_name", "").strip()

        if city_name:
            lat, lon = fetch_location_data(city_name)
            if lat is not None and lon is not None:
                forecast_data, condition, current_data = fetch_weather_data(lat, lon)
                if forecast_data is None:
                    error_message = "❌ Couldn't get weather forecast. Try again later."
                    condition = "default"
            else:
                error_message = f"❌ No results found for '{city_name}'."
        else:
            error_message = "❌ Please enter a city name."

    return render_template("index.html",
                           forecast=forecast_data,
                           error=error_message,
                           city=city_name,
                           condition=condition,
                           current=current_data)

if __name__ == "__main__":
    app.run(debug=True)
