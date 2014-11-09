# -*- coding: utf-8 -*-

from django.db import models
from django.contrib import admin

# Create your models here.
class OrganisationSettings(models.Model):
	def __str__(self):
		return self.subdom
	title = models.CharField(verbose_name = 'Название', max_length = 300)
	subdom = models.CharField(verbose_name = 'Субдомен', max_length = 30)

admin.site.register(OrganisationSettings)
