# events/models.py
from django.db import models
from django.utils import timezone

from users.models import User


class Event(models.Model):
    title = models.CharField(max_length=255, verbose_name='название')
    description = models.TextField(verbose_name='описание')
    date = models.DateTimeField(verbose_name='дата и время')
    location = models.CharField(max_length=255, verbose_name='место проведения')
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='organized_events',
                                  verbose_name='организатор')

    participants = models.ManyToManyField(User, related_name='registered_events', verbose_name='участники', blank=True)

    class Meta:
        verbose_name = 'мероприятие'
        verbose_name_plural = 'мероприятия'
        ordering = ('date',)

    def __str__(self):
        return self.title


class Registration(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='registrations', verbose_name='мероприятие')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='registrations', verbose_name='пользователь')
    registration_date = models.DateTimeField(default=timezone.now, verbose_name='дата записи')

    class Meta:
        unique_together = ['event', 'user']
        verbose_name = 'запись на мероприятие'
        verbose_name_plural = 'записи на мероприятия'

    def __str__(self):
        return f'{self.user} на {self.event} ({self.registration_date})'
