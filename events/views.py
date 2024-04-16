from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from events.models import Event, Registration
from events.serializers import EventSerializer, RegistrationSerializer
from events.tasks import send_event_notification, send_registration_notification, send_notify_registration_cancel
from users.permissions import IsOwnerProfile


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


class RegisterListAPIView(generics.ListAPIView):
    serializer_class = RegistrationSerializer
    queryset = Registration.objects.all()
    permission_classes = [IsOwnerProfile]


class CancelRegistrationAPIView(generics.DestroyAPIView):
    queryset = Registration.objects.all()
    permission_classes = [IsOwnerProfile]

    def destroy(self, request, *args, **kwargs):
        try:
            registration_id = self.kwargs['registration_id']
            registration = Registration.objects.get(pk=registration_id)
            registration.delete()
            return Response({"message": "Регистрация успешно отменена"}, status=status.HTTP_204_NO_CONTENT)
        except Registration.DoesNotExist:
            return Response({"error": "Регистрация не найдена"}, status=status.HTTP_404_NOT_FOUND)
