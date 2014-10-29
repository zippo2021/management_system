# -*- coding: utf-8 -*-
from django.db import models

# Create your models here.
'''
if event is a journey
'''
class JourneyData(models.Model):
    event = models.OneToOneField('events.admin_events.Event')
    tickets = models.ForeignKey('events.tickets.Ticket')
    departure_time = models.DateTimeField(verbose_name = 'Время отправления')
    info = models.CharField(verbose_name = 'Информация', blank = True)

class Ticket(models.Model):
    user = models.OneToOneField('dashboard.regular.RegularUser') # or any user? 
    price = models.IntegerField(verbose_name = 'Цена билета', blank = True)
    place = models.CharField(verbose_name = 'Место', blank = True)
    is_apart = models.BooleanField()
