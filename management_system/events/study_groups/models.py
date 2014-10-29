# -*- coding: utf-8 -*-
from django.db import models

# Create your models here.

#group with number and it's participants

class StudyGroup(models.Model):
    event = models.ForeignKey('events.admin_events.Event')
    label = models.CharField(verbose_name = 'Название/Номер')
    users = models.ManyToManyField('dashboard.regular.RegularUser')
