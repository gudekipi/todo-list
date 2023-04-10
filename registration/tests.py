from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from registration.serializers import UserSerializer

class RegistrationAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('register')

    def test_register_valid_payload(self):
        payload = {'username': 'testuser', 'password': 'testpass'}
        response = self.client.post(self.register_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.count(), 1)

    def test_register_invalid_payload(self):
        payload = {'username': '', 'password': ''}
        response = self.client.post(self.register_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'error': 'This field may not be blank.'})

    def test_register_invalid_username(self):
        payload = {'username': '', 'password': 'testpass'}
        response = self.client.post(self.register_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'error': 'This field may not be blank.'})

    def test_register_invalid_password(self):
        payload = {'username': 'testuser', 'password': ''}
        response = self.client.post(self.register_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'error': 'This field may not be blank.'})

    def test_register_duplicate_username(self):
        User.objects.create(username='testuser', password='testpass')
        payload = {'username': 'testuser', 'password': 'testpass2'}
        response = self.client.post(self.register_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'error': 'A user with that username already exists.'})
