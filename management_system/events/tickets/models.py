# -*- coding: utf-8 -*-
from django.db import models

# Create your models here.
class Ticket(models.Model):
    user = models.OneToOneField('regular.RegularUser') # or any user? 
    price = models.IntegerField(verbose_name = 'Цена билета', blank = True)
    place = models.CharField(verbose_name = 'Место',
							 blank = True,
							 max_length = 100,
	)
    is_apart = models.BooleanField()
