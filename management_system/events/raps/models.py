# -*- coding: utf-8 -*-
from django.db import models
from dashboard.teacher.models import Mentor
from dashboard.regular.models import RegularUser
# Create your models here.
class Rap(models.Model):
    author = models.ForeignKey(Mentor)
    receiver = models.ForeignKey(RegularUser)
    text = models.CharField(verbose_name = 'Замечание', max_length = 1000)
    is_sms = models.BooleanField()
