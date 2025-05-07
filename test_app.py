import unittest
from app import fetch_location_data, fetch_weather_data


class TestWeatherApp(unittest.TestCase):

    def test_fetch_location_valid_city(self):
        lat, lon = fetch_location_data("New York")
        self.assertIsNotNone(lat)
        self.assertIsNotNone(lon)

    def test_fetch_location_invalid_city(self):
        lat, lon = fetch_location_data("asdkfjasldkfjasldfj")  # gibberish
        self.assertIsNone(lat)
        self.assertIsNone(lon)

    def test_fetch_weather_valid_coords(self):
        forecast, condition, current = fetch_weather_data(40.7128, -74.0060)  # New York coords
        self.assertTrue(forecast)  # not empty
        self.assertIn(condition, ["sunny", "normal", "cold", "rainy"])
        self.assertIn("temperature", current)

if __name__ == '__main__':
    unittest.main()
