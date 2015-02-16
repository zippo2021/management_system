# -*- coding: utf-8 -*-


from django.forms import ModelForm, Form, BooleanField
from events.events_admin.models import Event, JourneyData, Result

class EventEditForm(ModelForm):
    class Meta:
        model = Event
        exclude = ['subject_workers',
                   'mentors',
                   'observers',
                   'is_private',
                   'is_payed',
                   'is_journey',
                   'is_active',
                  ]

class EventForm(ModelForm):
    class Meta:
        model = Event
        exclude = ['subject_workers',
                   'mentors',
                   'observers',
                   'is_active',
                   ]

class JourneyDataForm(ModelForm):
    class Meta:
        model = JourneyData
        exclude = ['event', 'tickets']

#should be cut from here !FIXIT!
class EventMailForm(Form):
    mail = BooleanField(label = 'Проводить рассылку')
