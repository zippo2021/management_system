# -*- coding: utf-8 -*-
from django.db import models
# Create your models here.

'''
Comments about user according to this event
'''
class PersonalComment(models.Model):
    event = models.ForeignKey('events_admin.Event',
							  related_name = 'PersonalComment')
    user = models.ForeignKey('regular.RegularUser',
							  related_name = 'PersonalComment')
    text = models.CharField(verbose_name = 'Комментарий', max_length = 1000)
