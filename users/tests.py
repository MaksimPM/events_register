from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()


class UserAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_user_registration(self):
        # Тест успешной регистрации пользователя
        response = self.client.post('/users/sign-up/', {
            'name': 'Test User',
            'email': 'test@example.com',
            'password': 'testpassword'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email='test@example.com').exists())

    def test_user_registration_duplicate_email(self):
        # Тест регистрации пользователя с уже существующим email
        User.objects.create_user(email='test@example.com', password='testpassword')
        response = self.client.post('/users/sign-up/', {
            'name': 'Another User',
            'email': 'test@example.com',
            'password': 'anotherpassword'
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['email'][0], 'Пользователь с таким email уже существует')

    def test_user_registration_missing_fields(self):
        # Тест регистрации пользователя с недостающими полями
        response = self.client.post('/users/sign-up/', {
            'email': 'test@example.com',
            'password': 'testpassword'
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_authentication(self):
        # Тест успешной аутентификации пользователя
        User.objects.create_user(email='test@example.com', password='testpassword')
        response = self.client.post('/users/sign-in/', {
            'email': 'test@example.com',
            'password': 'testpassword'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access_token', response.data)

    def test_user_authentication_failure(self):
        # Тест неудачной аутентификации пользователя (неверный пароль)
        User.objects.create_user(email='test@example.com', password='testpassword')
        response = self.client.post('/users/sign-in/', {
            'email': 'test@example.com',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_authentication_missing_credentials(self):
        # Тест аутентификации пользователя без указания email и пароля
        response = self.client.post('/users/sign-in/')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
