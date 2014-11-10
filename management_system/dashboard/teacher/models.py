# -*- coding: utf-8 -*-
from django.db import models
from django.contrib import admin
# Create your models here.

class Teacher(models.Model):
	def __str__(self):
		return self.data.__str__()
	data = models.OneToOneField('userdata.UserData', related_name = 'Teacher')
	info = models.CharField(verbose_name = 'Информация' , max_length = 1000)

admin.site.register(Teacher)
