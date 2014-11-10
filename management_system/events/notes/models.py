# -*- coding: utf-8 -*-
from django.db import models

# Create your models here.
class Note(models.Model):
	author = models.ForeignKey('teacher.Teacher', related_name = 'Note')
	receiver = models.ForeignKey('regular.RegularUser', related_name = 'Note')
	text = models.CharField(verbose_name = 'Запись', max_length = 1000)

