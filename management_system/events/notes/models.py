# -*- coding: utf-8 -*-
from django.db import models

from dashboard.teacher.models import Teacher
from dashboard.regular.models import RegularUser
# Create your models here.
class Note(models.Model):
	author = models.ForeignKey(Teacher)
	receiver = models.ForeignKey(RegularUser)
	text = models.CharField(verbose_name = 'Запись', max_length = 1000)

