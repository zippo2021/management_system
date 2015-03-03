# -*- coding: utf-8 -*-
from django.db import models


class Subject(models.Model):
    name = models.CharField(max_length=100)
    event = models.ForeignKey('events_admin.Event', related_name="subject")

    class Meta:
        unique_together = ("event", "name")

    def __unicode__(self):
        return self.name


class Lesson(models.Model):
    subject = models.ForeignKey(Subject, related_name='lesson')
    title = models.CharField(max_length=100)
    comment = models.TextField(blank=True, null=True)
    teacher = models.ForeignKey('teacher.Teacher', related_name='lesson')
    group = models.ForeignKey('study_groups.StudyGroup', related_name='lesson')
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    place = models.CharField(max_length=100, blank=True, null=True)
    event = models.ForeignKey('events_admin.Event', related_name='lesson')

    def __unicode__(self):
        return u'%s (%s)' % (self.title, self.subject.name)


class Homework(models.Model):
    title = models.CharField(max_length=100)
    comment = models.TextField(blank=True, null=True)
    to_lesson = models.ForeignKey(Lesson, related_name='homework', on_delete=models.DO_NOTHING)

    def __unicode__(self):
        return u'%s' % self.title


class Mark(models.Model):
    mark = models.PositiveSmallIntegerField()
    comment = models.CharField(max_length=100, blank=True, null=True)
    lesson = models.ForeignKey(Lesson, related_name='mark', on_delete=models.DO_NOTHING)
    pupil = models.ForeignKey('regular.RegularUser', related_name='mark', on_delete=models.DO_NOTHING)

    def __unicode__(self):
        return u'%u' % self.mark
