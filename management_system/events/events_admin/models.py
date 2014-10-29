# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

from dashboard.regular.models import Regular
from dashboard.teacher.models import EventWorker, Teacher, Mentor, Observer


class Event(models.Model):
    name = models.CharField(verbose_name = 'Название', max_length = 100)
    comment = models.CharFielf(verbose_name = 'Комментарий',
			       max_length = 1000, blank = True)
    place = models.CharField(verbose_name = 'Место проведения',
			     max_length = 100)
    opened = models.DateField(verbose_name = 'Создано')
    closed = models.DateField(verbose_name = 'Закрыто')
    is_private = models.BooleanField()
    is_journey = models.BooleanField()
    is_payed = models.BooleanField()
    event_workers = models.ManyToManyField(EventWorker)
    subject_workers = models.ManyToManyField(SubjectWorker)
    mentors = models.ManyToManyField(Mentor)
    observers = models.ManyToManyField(Observer)


'''
if event is private
'''
class Requests(models.Model):
    event = models.ForeignKey(Event)
    users = models.ManyToManyField(RegularUser)

class Contract(models.Model):
    event = models.ForeignKey(Event)
    user = models.ForeignKey(RegularUser)
    '''
    it has to be completed
    '''
