# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
from dashboard.teacher.models import Teacher


class Event(models.Model):
    def __unicode__ (self):
        return self.name
    name = models.CharField(verbose_name = 'Название', max_length = 100)
    comment = models.TextField(verbose_name = 'Комментарий',
			       max_length = 1000, blank = True)
    place = models.CharField(verbose_name = 'Место проведения',
			     max_length = 100)
    opened = models.DateField(verbose_name = 'Создано')
    closed = models.DateField(verbose_name = 'Закрыто')
    is_private = models.BooleanField(verbose_name = 'Добавление по заявкам')
    is_journey = models.BooleanField(verbose_name = 'Выездное')
    is_payed = models.BooleanField(verbose_name = 'Оплачиваемое')
    has_journal = models.BooleanField(verbose_name = 'Вести журнал')
    event_workers = models.ManyToManyField('event_worker.EventWorker',
                                          verbose_name = 'Управляющие событием')
    teachers = models.ManyToManyField('teacher.Teacher')
    mentors = models.ManyToManyField('mentor.Mentor')
    observers = models.ManyToManyField('observer.Observer')
    is_active = models.BooleanField()
admin.site.register(Event)


class JourneyData(models.Model):
    def __unicode__(self):
        return self.event.name
    event = models.OneToOneField('events_admin.Event',
								 related_name = 'JourneyData')
    tickets = models.ForeignKey('tickets.Ticket', related_name = 'JourneyData',
                                blank = True, null = True)
    departure_time = models.DateTimeField(verbose_name = 'Время отправления')
    info = models.TextField(verbose_name = 'Информация',
                            blank = True,
                            max_length = 1000,
    )
    
admin.site.register(JourneyData)




class Contract(models.Model):
    event = models.ForeignKey(Event, related_name = 'Contract')
    user = models.ForeignKey('regular.RegularUser', related_name = 'Contract')
