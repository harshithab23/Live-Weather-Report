import unittest
from app import app, fetch_weather_data  # Adjust if the import path differs

class RegressionTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.client.testing = True

    def test_homepage_still_works(self):
        """Homepage should still load after changes"""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Weather Report", response.data)

    def test_valid_city_forecast_structure(self):
        """Ensure forecast structure is correct for valid coordinates (Delhi)"""
        forecast, summary, current_weather = fetch_weather_data(28.61, 77.23)  # Delhi

        self.assertIsInstance(forecast, list)
        self.assertGreater(len(forecast), 0)
        self.assertIn("date", forecast[0])
        self.assertIn("temp_max", forecast[0])
        self.assertIn("temp_min", forecast[0])
        self.assertIn("humidity", forecast[0])
        self.assertIn("wind_speed", forecast[0])

        self.assertIsInstance(summary, str)
        self.assertIsInstance(current_weather, dict)

    def test_invalid_city_handled(self):
        """Test that an invalid location doesn't crash the app"""
        forecast, summary, current_weather = fetch_weather_data(0.0, 0.0)
        
        self.assertIsInstance(forecast, list)
        self.assertGreater(len(forecast), 0)  # Since even (0,0) returns real data from open-meteo

        self.assertIsInstance(summary, str)
        self.assertIsInstance(current_weather, dict)

if __name__ == '__main__':
    unittest.main()
