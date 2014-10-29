# -*- coding: utf-8 -*-
from django.db import models

# Create your models here.
class Note(models.Model):
	author = models.ForeignKey('teacher.Teacher')
	receiver = models.ForeignKey('regular.RegularUser')
	text = models.CharField(verbose_name = 'Запись', max_length = 1000)

