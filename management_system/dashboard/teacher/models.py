# -*- coding: utf-8 -*-
from django.db import models
# Create your models here.

class Teacher(models.Model):
	data = models.OneToOneField('userdata.UserData')
	info = models.CharField(verbose_name = 'Информация' , max_length = 1000)
