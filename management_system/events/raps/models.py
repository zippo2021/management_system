# -*- coding: utf-8 -*-
from django.db import models
# Create your models here.
class Rap(models.Model):
    author = models.ForeignKey('dashboard.mentor.Mentor')
    receiver = models.ForeignKey('dashboard.regular.RegularUser')
    text = models.CharField(verbose_name = 'Замечание', max_length = 1000)
    is_sms = models.BooleanField()
