from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
import json

class RecommendationViewTests(TestCase):
    def setUp(self):
        # Set up a user for testing
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_get_recommendations_valid_user(self):
        # Send GET request to the recommendations endpoint
        url = reverse('recommendations', kwargs={'user_id': self.user.id})
        response = self.client.get(url)

        # Check HTTP status
        self.assertEqual(response.status_code, 200)

        # Parse JSON response
        data = response.json()

        # Check for expected keys
        self.assertIn('recommendations', data)
        self.assertEqual(data['user'], self.user.username)
        self.assertEqual(data['user_id'], self.user.id)

        # Check the recommendations are a list of 5 integers
        self.assertIsInstance(data['recommendations'], list)
        self.assertEqual(len(data['recommendations']), 5)
        self.assertTrue(all(isinstance(i, int) for i in data['recommendations']))

    def test_get_recommendations_invalid_user(self):
        # Use a user ID that doesn't exist
        invalid_user_id = 9999
        url = reverse('recommendations', kwargs={'user_id': invalid_user_id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"error": "User not found."})

