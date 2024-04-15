from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from users.models import User
from .models import Event, Registration


@shared_task
def send_event_notification(event_id):
    event = Event.objects.get(pk=event_id)
    all_users = User.objects.all()

    subject = f'Уведомление о мероприятии: {event.title}'
    message = f'Привет!\n\n' \
              f'Приглашаем вас принять участие в нашем мероприятии "{event.title}". ' \
              f'Оно состоится {event.date} по адресу: {event.location}.\n\n' \
              f'Подробности события:\n\n' \
              f'{event.description}\n\n' \
              f'Ждем вас!\n\n' \
              f'Организатор: {event.organizer.name}\n' \
              f'Контактный email: {event.organizer.email}'
    from_email = settings.EMAIL_HOST_USER
    to_email = [all_users.email]

    for user in all_users:
        send_mail(subject, message, from_email, to_email)


@shared_task
def send_registration_notification(registration_id):
    registration = Registration.objects.get(pk=registration_id)
    event = registration.event
    user = registration.user

    subject = f'Уведомление о записи на мероприятие: {event.title}'
    message = f'Привет, {user.name}!\n\n' \
              f'Вы успешно записались на мероприятие "{event.title}". ' \
              f'Оно состоится {event.date} по адресу: {event.location}.\n\n' \
              f'Ждем вас!\n\n' \
              f'Организатор: {event.organizer.name}\n' \
              f'Контактный email: {event.organizer.email}'
    from_email = settings.EMAIL_HOST_USER
    to_email = [user.email]
    html_message = render_to_string('registration_notification_email.html', {'event': event})
    plain_message = strip_tags(html_message)

    send_mail(subject, plain_message, from_email, to_email, html_message=html_message)


@shared_task
def send_cancel_registration_notification(registration_id):
    registration = Registration.objects.get(pk=registration_id)
    event = registration.event
    user = registration.user

    subject = f'Уведомление об отмене записи на мероприятие: {event.title}'
    message = f'Привет, {user.name}!\n\n' \
              f'Ваша запись на мероприятие "{event.title}" была отменена.\n\n' \
              f'Если у вас возникли вопросы, пожалуйста, свяжитесь с организатором мероприятия: {event.organizer.name}\n' \
              f'Контактный email: {event.organizer.email}'
    from_email = settings.EMAIL_HOST_USER
    to_email = [user.email]
    html_message = render_to_string('cancel_registration_notification_email.html', {'event': event})
    plain_message = strip_tags(html_message)

    send_mail(subject, plain_message, from_email, to_email, html_message=html_message)
