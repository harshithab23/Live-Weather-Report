Live Weather Report
This is a Flask-based web application that displays real-time weather conditions and a 7-day weather forecast based on a user's city input. It uses the [Open-Meteo Geocoding API](https://open-meteo.com/en/docs/geocoding-api) to fetch latitude and longitude, and the [Open-Meteo Weather API](https://open-meteo.com/en/docs) to retrieve weather data.

Features
- Fetches current weather (temperature, windspeed)
- Displays 7-day forecast with:
  - Max and Min Temperature
  - Humidity
  - Wind Speed
- Background video changes based on the weather condition (e.g. sunny, rainy, cold and normal)
- Built-in error handling
- Includes a loading spinner during API fetch
- Supports CI/CD using GitHub Actions

 Tech Stack
- Python (Flask)
- HTML5/CSS3
- JavaScript (for loader)
- Open-Meteo API
- GitHub Actions for CI/CD
