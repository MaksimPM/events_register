from celery import shared_task
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.utils import formats

from users.models import User
from .models import Event, Registration


@shared_task
def send_event_notification(event_id):
    event = Event.objects.get(pk=event_id)
    all_users = User.objects.all()
    print(f'Уведомление отправлено - {all_users}')

    subject = f'Уведомление о мероприятии: {event.title}'
    message = f'Привет!\n\n' \
              f'Приглашаем вас принять участие в нашем мероприятии "{event.title}".\n' \
              f'Оно состоится {formats.date_format(event.date, "DATETIME_FORMAT")}\n' \
              f'По адресу: {event.location}.\n\n' \
              f'Подробности события:\n\n' \
              f'{event.description}\n\n' \
              f'Ждем вас!\n\n' \
              f'Организатор: {event.organizer.name}\n' \
              f'Контактный email: {event.organizer.email}'
    from_email = settings.EMAIL_HOST_USER
    to_email = [user.email for user in all_users]

    send_mail(subject, message, from_email, to_email)


@shared_task
def send_registration_notification(registration_id):
    registration = Registration.objects.get(pk=registration_id)
    event = registration.event
    user = registration.user
    print(f'Уведомление о записи на мероприятие отправлено - {user.email}')

    subject = f'Уведомление о записи на мероприятие: {event.title}'
    message = f'Привет, {user.name}!\n\n' \
              f'Вы успешно записались на мероприятие "{event.title}".\n' \
              f'Оно состоится {formats.date_format(event.date, "DATETIME_FORMAT")}\n' \
              f'По адресу: {event.location}.\n\n' \
              f'Ждем вас!\n\n' \
              f'Организатор: {event.organizer.name}\n' \
              f'Контактный email: {event.organizer.email}'
    from_email = settings.EMAIL_HOST_USER
    to_email = [user.email]

    send_mail(subject, message, from_email, to_email)
