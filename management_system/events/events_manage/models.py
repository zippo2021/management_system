#-*- coding: utf-8 -*-

from django.db import models
from events.events_admin.models import Event
from events.price_groups.models import PriceGroup
from django.contrib import admin

class Result(models.Model):
    event = models.ForeignKey(Event, related_name = 'Result')
    user = models.ForeignKey('regular.RegularUser', related_name = 'Result')
    result = models.CharField(verbose_name = 'Результат',
                              max_length = 1000,    
    )

class EmailTemplate(models.Model):
    event = models.ForeignKey(Event, related_name = 'AcceptanceEmailTemplate')
    text = models.TextField(verbose_name = 'Результат',
                              max_length = 4000,
    )
admin.site.register(EmailTemplate)

class Request(models.Model):
    status = models.CharField(verbose_name = 'Статус',
                            blank = True,
                            max_length = 1000,
    )
    event = models.ForeignKey(Event, related_name = 'Request')
    user = models.ForeignKey('regular.RegularUser',
			   related_name = 'Request')
    price_group = models.ForeignKey(PriceGroup,
                                    related_name = 'Request',
                                    null = True)
admin.site.register(Request)
