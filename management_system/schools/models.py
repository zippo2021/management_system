# -*- coding: utf-8 -*-
from django.db import models

# Create your models here.

class School(models.Model):
    def __unicode__(self):
        return self.name+' '+self.city
    name = models.CharField(verbose_name = 'Название', max_length = 100)
    country = models.CharField(verbose_name = 'Страна', max_length = 30)
    city = models.CharField(verbose_name = 'Город', max_length = 30)
    approved = models.BooleanField(default = False)
