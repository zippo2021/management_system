# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
from dashboard.teacher.models import Teacher


class Event(models.Model):
    def __str__ (self):
        return self.name.encode('utf-8')
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
    teachers = models.ManyToManyField('teacher.Teacher')
    mentors = models.ManyToManyField('mentor.Mentor')
    observers = models.ManyToManyField('observer.Observer')
    
admin.site.register(Event)


class JourneyData(models.Model):
    event = models.OneToOneField('events_admin.Event',
								 related_name = 'JourneyData')
    tickets = models.ForeignKey('tickets.Ticket', related_name = 'JourneyData',
                                blank = True, null = True)
    departure_time = models.DateTimeField(verbose_name = 'Время отправления')
    info = models.CharField(verbose_name = 'Информация',
                            blank = True,
                            max_length = 1000,
    )
    
admin.site.register(JourneyData)


'''
if event is private
'''
class Requests(models.Model):
    event = models.ForeignKey(Event, related_name = 'Requests')
    users = models.ManyToManyField('regular.RegularUser',
								   related_name = 'Requests')

class Contract(models.Model):
    event = models.ForeignKey(Event, related_name = 'Contract')
    user = models.ForeignKey('regular.RegularUser', related_name = 'Contract')
    '''
    it has to be completed
    '''
