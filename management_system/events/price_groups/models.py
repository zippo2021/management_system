# -*- coding: utf-8 -*-
from django.db import models
from events_admin.models import Event
from dashboard.regular.models import RegularUser
# Create your models here.
'''
price and participants applied for this price
'''
class PriceGroup(models.Model):
    event = models.ForeignKey(Event)
    price = models.IntegerField(verbose_name = 'Стоимость')
    users = models.ManyToManyField(RegularUser)
    
