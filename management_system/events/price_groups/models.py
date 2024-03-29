# -*- coding: utf-8 -*-
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib import admin
from events.events_admin.models import Event
from django.contrib import admin

class PriceGroup(models.Model):
    def __unicode__ (self):
        if self.price == 0:
            return u'бесплатно'
        else:
            return unicode(self.price) + u' р.'
            _
    event = models.ForeignKey('events_admin.Event', related_name = 'PriceGroup')
    price = models.IntegerField(verbose_name = 'Стоимость')
    class Meta:
        unique_together = ('price','event')

admin.site.register(PriceGroup)

@receiver(post_save, sender = Event)
def create_price_group_free(instance, created, **kwargs):
    if created:
        group = PriceGroup(event = instance, price = 0)
        group.save()

