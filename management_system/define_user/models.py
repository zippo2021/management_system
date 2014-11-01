# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class DefineUserRequest(models.Model):
	user = models.OneToOneField(User, related_name = 'DefineUserRequest')
	teacher = models.BooleanField(verbose_name = 'Учитель')
	event_worker = models.BooleanField(verbose_name = 'Работник Событий')
	observer = models.BooleanField(verbose_name = 'Наблюдатель')
	mentor = models.BooleanField(verbose_name = 'Воспитатель')
