from django.urls import path

from events.apps import EventsConfig
from events.views import EventListCreateAPIView, EventDetailAPIView, RegisterToEventAPIView, CancelRegistrationAPIView, \
    index

app_name = EventsConfig.name

urlpatterns = [
    path('', index, name='index'),
    path('events/', EventListCreateAPIView.as_view(), name='event-list'),
    path('events/<int:pk>/', EventDetailAPIView.as_view(), name='event-detail'),
    path('<int:event_id>/register/', RegisterToEventAPIView.as_view(), name='register-to-event'),
    path('<int:event_id>/cancel-registration/', CancelRegistrationAPIView.as_view(), name='cancel-registration'),
]
