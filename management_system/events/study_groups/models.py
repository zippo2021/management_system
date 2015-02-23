# -*- coding: utf-8 -*-
from django.db import models

# Create your models here.

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