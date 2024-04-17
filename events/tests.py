from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken

from events.models import Event, Registration


class EventAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create(email='test@example.com', password='testpassword')
        self.access_token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.event = None
        self.registration = None

    def test_create_event(self):
        # Тест успешного создания мероприятия
        response = self.client.post('/events/', {
            'title': 'Test Event',
            'description': 'This is a test event',
            'date': '2024-04-15 12:00',
            'location': 'Test Location',
            'organizer': self.user.pk
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Event.objects.filter(title='Test Event').exists())

    def test_create_event_missing_fields(self):
        # Тест создания мероприятия с недостающими полями
        response = self.client.post('/events/', {
            'title': 'Test Event',
            'description': 'This is a test event',
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_events(self):
        # Тест успешного получения списка мероприятий
        response = self.client.get('/events/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_event_detail(self):
        # Тест успешного получения деталей мероприятия
        self.event = Event.objects.create(
            title='Test Event',
            description='This is a test event',
            date='2024-04-15 12:00',
            location='Test Location',
            organizer=self.user
        )
        response = self.client.get(f'/events/{self.event.pk}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Event')

    def test_register_to_event(self):
        # Тест успешной регистрации на мероприятие
        self.test_create_event()
        event = Event.objects.get(title='Test Event')
        response = self.client.post(f'/{event.pk}/register/', {'event': event.pk, 'user': self.user.pk})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.registration = Registration.objects.get(event=event, user=self.user)

    def test_get_registration(self):
        # Тест успешного получения списка регистраций
        response = self.client.get('/register/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cancel_registration(self):
        # Тест успешной отмены регистрации на мероприятие
        self.test_register_to_event()
        if not self.registration:
            self.fail('The registration must be created in test_register_to_event')
        response = self.client.delete(f'/{self.registration.event.pk}/cancel-registration/{self.registration.pk}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
