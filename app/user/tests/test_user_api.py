from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

# Create your tests here.
CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')

def create_user(**params):
    return get_user_model().objects.create_user(**params)

class PublicUserApiTests(TestCase):
    """Test the users api (public)"""
    def setUp(self):
        self.client = APIClient()


    def test_create_valid_user_success(self):
        """Test creating user with valid payload is successful"""
        payload = {
            'email': 'test@email.com',
            'password': 'testpass',
            'name': 'user'
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_exists(self):
        """Test creating a user that is already exists fails"""
        payload = {
            'email': 'test@email.com',
            'password': 'testpass',
            'name': 'user'
        }
        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Test that the password must be more than 5 characters"""
        payload = {
            'email': 'test@email.com',
            'password': 'test',
            'name': 'user'
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(email=payload['email']).exists()
        
        self.assertFalse(user_exists)

    def test_create_user_token(self):
        """Test that a token is created for user"""
        payload = {
            'email': 'testtest@emailvd.com',
            'password': 'testpassword',
            'name': 'username'
        }
        create_user(**payload)

        res = self.client.post(TOKEN_URL, payload)
        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
    
    def test_create_user_token_with_invalid_credentials(self):
        """Test that a token is not created if invalid credentials are given"""
        create_user(email='test@email.com', password='testpass', name='user')
        payload = {
            'email': 'test@eml.com',
            'password': 'few',
            'name': 'usercwq'
        }

        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_create_token_no_user(self):
        """Test that a token is not created if user doesn`t exists"""
        payload = {
            'email': 'test@email.com',
            'password': 'testpass',
        }

        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        """Test that email and password are required"""
        payload = {
            'email': 'test',
            'password': '',
            'name': 'user'
        }

        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


