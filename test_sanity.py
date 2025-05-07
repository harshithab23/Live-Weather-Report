import unittest
from app import app 

class SanityTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.client.testing = True

    def test_homepage_loads(self):
        """Check if homepage loads correctly"""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Weather Report", response.data)

    def test_forecast_search_post(self):
        """Basic POST test with a valid city"""
        response = self.client.post("/", data={"city_name": "London"})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Forecast for", response.data)

if __name__ == "__main__":
    unittest.main()
