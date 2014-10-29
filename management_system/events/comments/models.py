# -*- coding: utf-8 -*-
from django.db import models
# Create your models here.

'''
Comments about user according to this event
'''
class PersonalComment(models.Model):
    event = models.ForeignKey('events.events_admin.Event')
    user = models.ForeignKey('dashboard.regular.RegularUser')
    text = models.CharField(verbose_name = 'Комментарий', max_length = 1000)
