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
        generated_password = User.objects.make_random_password()
        response = self.client.post('/users/sign-up/', {
            'name': 'Test User',
            'email': 'test@example.com',
            'password': generated_password
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email='test@example.com').exists())

    def test_user_registration_missing_fields(self):
        # Тест регистрации пользователя с недостающими полями
        response = self.client.post('/users/sign-up/', {
            'email': 'test@example.com',
            'password': 'testpassword'
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_authentication(self):
        # Тест успешной аутентификации пользователя
        user = User.objects.create(email='test@example.com')
        generated_password = User.objects.make_random_password()
        user.set_password(generated_password)
        user.save()

        # Аутентификация пользователя
        response = self.client.post('/users/sign-in/', {
            'email': 'test@example.com',
            'password': generated_password
        })

        # Проверка успешности аутентификации
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('access_token' in response.data)

    def test_user_authentication_failure(self):
        # Тест неудачной аутентификации пользователя (неверный пароль)
        User.objects.create(email='test@example.com', password='testpassword')
        response = self.client.post('/users/sign-in/', {
            'email': 'test@example.com',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_authentication_missing_credentials(self):
        # Тест аутентификации пользователя без указания email и пароля
        response = self.client.post('/users/sign-in/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
