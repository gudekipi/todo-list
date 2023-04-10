from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, force_authenticate
from django.contrib.auth.models import User
from registration.serializers import UserSerializer

# Create your tests here.
class LoginLogoutUserTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')

    def test_login_view_with_valid_credentials(self):
        data = {'username': 'testuser', 'password': 'testpass'}
        response = self.client.post(self.login_url, data)
       
        self.assertEqual(response.status_code, 200)
        self.assertIn('token', response.data)
        
        token = response.data['token']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)        
        
    def test_login_view_with_invalid_credentials(self):
        data = {'username': 'testuser', 'password': 'wrongpass'}
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, 403)
        
    def test_logout_view_with_authenticated_user(self):
        self.client.force_authenticate(self.user)
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {'message': 'Logged out successfully'})
        
