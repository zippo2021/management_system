# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

from dashboard.teacher.models import Teacher


class Event(models.Model):
    name = models.CharField(verbose_name = 'Название', max_length = 100)
    comment = models.CharField(verbose_name = 'Комментарий',
			       max_length = 1000, blank = True)
    place = models.CharField(verbose_name = 'Место проведения',
			     max_length = 100)
    opened = models.DateField(verbose_name = 'Создано')
    closed = models.DateField(verbose_name = 'Закрыто')
    is_private = models.BooleanField()
    is_journey = models.BooleanField()
    is_payed = models.BooleanField()
    event_workers = models.ManyToManyField('event_worker.EventWorker')
    subject_workers = models.ManyToManyField('teacher.Teacher')
    mentors = models.ManyToManyField('mentor.Mentor')
    observers = models.ManyToManyField('observer.Observer')


class JourneyData(models.Model):
    event = models.OneToOneField('events_admin.Event')
    tickets = models.ForeignKey('tickets.Ticket')
    departure_time = models.DateTimeField(verbose_name = 'Время отправления')
    info = models.CharField(verbose_name = 'Информация',
                            blank = True,
                            max_length = 1000,
    )


'''
if event is private
'''
class Requests(models.Model):
    event = models.ForeignKey(Event)
    users = models.ManyToManyField('regular.RegularUser')

class Contract(models.Model):
    event = models.ForeignKey(Event)
    user = models.ForeignKey('regular.RegularUser')
    '''
    it has to be completed
    '''
