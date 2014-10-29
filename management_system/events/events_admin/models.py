# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

from dashboard.teacher.models import Teacher

class EventWorker(models.Model):
    data = models.OneToOneField('dashboard.regular.UserData')

class Mentor(models.Model):
    data = models.OneToOneField('dashboard.regular.UserData')

class Observer(models.Model):
    data = models.OneToOneField('dashboard.regular.UserData')


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
    event_workers = models.ManyToManyField(EventWorker)
    subject_workers = models.ManyToManyField('dashboard.teacher.Teacher')
    mentors = models.ManyToManyField(Mentor)
    observers = models.ManyToManyField(Observer)


'''
if event is private
'''
class Requests(models.Model):
    event = models.ForeignKey(Event)
    users = models.ManyToManyField('dashboard.regular.RegularUser')

class Contract(models.Model):
    event = models.ForeignKey(Event)
    user = models.ForeignKey('dashboard.regular.RegularUser')
    '''
    it has to be completed
    '''
