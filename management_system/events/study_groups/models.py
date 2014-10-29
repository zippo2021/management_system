# -*- coding: utf-8 -*-
from django.db import models

from django.contrib.auth.models import User
from dashboard.regular.models import RegularUser
from events_admin.models import Event
# Create your models here.

#group with number and it's participants

class StudyGroup(models.Model):
    event = models.ForeignKey(Event)
    label = models.CharField(verbose_name = 'Название/Номер')
    users = models.ManyToManyField(RegularUser)
