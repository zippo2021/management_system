# -*- coding: utf-8 -*-
from django.db import models
# Create your models here.
class Rap(models.Model):
    author = models.ForeignKey('mentor.Mentor',related_name = 'Rap')
    receiver = models.ForeignKey('regular.RegularUser', related_name = 'Rap')
    text = models.CharField(verbose_name = 'Замечание', max_length = 1000)
    is_sms = models.BooleanField()
