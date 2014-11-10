# -*- coding: utf-8 -*-
from django.db import models
# Create your models here.
'''
price and participants applied for this price
'''
class PriceGroup(models.Model):
    event = models.ForeignKey('events_admin.Event', related_name = 'PriceGroup')
    price = models.IntegerField(verbose_name = 'Стоимость')
    users = models.ManyToManyField('regular.RegularUser',
								   related_name = 'PriceGroup')
    
