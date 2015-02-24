# -*- coding: utf-8 -*-
from django.db import models
from django.contrib import admin
# Create your models here.

class Teacher(models.Model):
    def __unicode__ (self):
        return self.data.last_name +' '+ self.data.first_name
    data = models.OneToOneField('userdata.UserData', related_name = 'Teacher')
    info = models.TextField(verbose_name = 'Информация', max_length = 1000, blank = True)
    is_active = models.BooleanField(default = False)

admin.site.register(Teacher)
