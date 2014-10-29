# -*- coding: utf-8 -*-
from django.db import models

from dashboard.regular.models import RegularUser
from events_admin.models import Event
# Create your models here.
'''
if event is a journey
'''
class JourneyData(models.Model):
    event = models.OneToOne(Event)
    tickets = models.ForeignKey(Ticket)
    departure_time = models.DateTimeField(verbose_name = 'Время отправления')
    info = models.CharField(verbose_name = 'Информация', blank = True)

class Ticket(models.Model):
    user = models.OneToOneField(RegularUser) # or any user? 
    price = models.IntegerField(verbose_name = 'Цена билета', blank = True)
    place = nodels.CharField(verbose_name = 'Место', blank = True)
    is_apart = models.BooleanField()
