# -*- coding: utf-8 -*-


from django.forms import ModelForm
from event.event_admin.models import Event, JourneyData

class EventForm(ModelForm):
    class Meta:
        model = Event
        exclude = ['subject_workers',
                   'mentors',
                   'observers',
                   ]

class JourneyDataForm(ModelForm):
    class Meta:
        model = JourneyData
        exclude = ['event']
