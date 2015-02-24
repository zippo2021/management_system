# -*- coding: utf-8 -*-
from django.db import models
from events.events_admin.models import Event
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib import admin

#group with number and it's participants


class StudyGroup(models.Model):
    event = models.ForeignKey('events_admin.Event', related_name='StudyGroup')
    label = models.CharField(verbose_name='Название/Номер', max_length=100)
    users = models.ManyToManyField('regular.RegularUser',
                                   related_name='StudyGroup')

    class Meta:
        unique_together = ("event", "label")

    def __unicode__(self):
        return self.label
#admin.site.register(StudyGroup)


@receiver(post_save, sender = Event)
def create_study_group_all(instance, created, **kwargs):
    if created:
        group = StudyGroup(event = instance, label = 'All')
        group.save()
