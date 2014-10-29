# -*- coding: utf-8 -*-
from django.db import models
from dashboard.regular.models import UserData
# Create your models here.
class EventWorker(models.Model):
	data = models.OneToOneField(UserData)

class Teacher(models.Model):
	data = models.OneToOneField(UserData)
	info = models.CharField(verbose_name = 'Информация' , max_length = 1000)

class Mentor(models.Model):
        data = models.OneToOneField(UserData)

class Observer(models.Model):
	data = models.OneToOneField(UserData)


