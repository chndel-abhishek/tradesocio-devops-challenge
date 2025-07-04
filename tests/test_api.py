import unittest
from app.main import app

class APITestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_api_post(self):
        response = self.app.post('/api', json={'username': 'xyz', 'password': 'xyz'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome to our demo API', response.data)

if __name__ == '__main__':
    unittest.main()