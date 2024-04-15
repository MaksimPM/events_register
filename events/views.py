from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from events.models import Event, Registration
from events.serializers import EventSerializer, RegistrationSerializer
from events.tasks import send_event_notification, send_registration_notification, send_cancel_registration_notification


def index(request):
    return render(request, 'events/index.html')


class EventListCreateAPIView(generics.ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        event = serializer.save(organizer=self.request.user)
        send_event_notification.delay(event.id)


class EventDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]


class RegisterToEventAPIView(generics.CreateAPIView):
    serializer_class = RegistrationSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        event_id = self.kwargs['event_id']
        event = Event.objects.get(pk=event_id)
        registration = serializer.save(event=event, user=self.request.user)
        send_registration_notification.delay(registration.id)


class CancelRegistrationAPIView(generics.DestroyAPIView):
    queryset = Registration.objects.all()
    permission_classes = [IsAuthenticated]

    def get_object(self):
        event_id = self.kwargs['event_id']
        return self.queryset.get(event_id=event_id, user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        send_cancel_registration_notification.delay(instance.id)
        return Response(status=status.HTTP_204_NO_CONTENT)
