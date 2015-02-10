# -*- coding: utf-8 -*-


from django.forms import ModelForm, Form, BooleanField
from events.events_admin.models import Event, JourneyData

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
        exclude = ['event', 'tickets']

#should be cut from here !FIXIT!
class EventMailForm(Form):
    mail = BooleanField(label = 'Проводить рассылку')
