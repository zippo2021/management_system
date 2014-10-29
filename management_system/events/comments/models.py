# -*- coding: utf-8 -*-
from django.db import models
from events_admin.models import Event
from dashboard.regular.models import RegularUser
# Create your models here.

'''
Comments about user according to this event
'''
class PersonalComment(models.Model):
    event = models.ForeignKey(Event)
    user = models.ForeignKey(RegularUser)
    text = models.CharField(verbose_name = 'Комментарий', max_length = 1000)
