from django.urls import path

from events.apps import EventsConfig
from events.views import EventListCreateAPIView, EventDetailAPIView, RegisterToEventAPIView, CancelRegistrationAPIView,\
    RegisterListAPIView

app_name = EventsConfig.name

urlpatterns = [
    path('events/', EventListCreateAPIView.as_view(), name='event-list'),
    path('events/<int:pk>/', EventDetailAPIView.as_view(), name='event-detail'),
    path('register/', RegisterListAPIView.as_view(), name='register-list'),
    path('<int:event_id>/register/', RegisterToEventAPIView.as_view(), name='register-to-event'),
    path('<int:event_id>/cancel-registration/<int:registration_id>/', CancelRegistrationAPIView.as_view(),
         name='cancel-registration'),
]
