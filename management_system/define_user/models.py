# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin

# Create your models here.
class DefineUserRequest(models.Model):
	def __str__(self):
		return self.user.__str__()
	user = models.OneToOneField(User, related_name = 'DefineUserRequest')
	info = models.CharField(verbose_name = 'Информация', max_length = 1000)
	teacher = models.BooleanField(verbose_name = 'Учитель')
	event_worker = models.BooleanField(verbose_name = 'Работник Событий')
	observer = models.BooleanField(verbose_name = 'Наблюдатель')
	mentor = models.BooleanField(verbose_name = 'Воспитатель')

admin.site.register(DefineUserRequest)
