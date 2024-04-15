from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Event
from users.models import User


class EventAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email='test@example.com', password='testpassword')
        self.client.force_authenticate(user=self.user)

    def test_create_event(self):
        # Тест успешного создания мероприятия
        response = self.client.post('', {
            'title': 'Test Event',
            'description': 'This is a test event',
            'date': '2024-04-15T12:00:00Z',
            'location': 'Test Location'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Event.objects.filter(title='Test Event').exists())

    def test_create_event_missing_fields(self):
        # Тест создания мероприятия с недостающими полями
        response = self.client.post('', {
            'title': 'Test Event',
            'description': 'This is a test event',
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_events(self):
        # Тест успешного получения списка мероприятий
        response = self.client.get('')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_event_detail(self):
        # Тест успешного получения деталей мероприятия
        event = Event.objects.create(
            title='Test Event',
            description='This is a test event',
            date='2024-04-15T12:00:00Z',
            location='Test Location',
            organizer=self.user
        )
        response = self.client.get(f'/{event.pk}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Event')
