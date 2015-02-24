# -*- coding: utf-8 -*-

from dashboard.event_worker.models import EventWorker
from django.forms import ModelForm, Form, BooleanField, ModelMultipleChoiceField
from events.events_admin.models import Event, JourneyData
from events.events_manage.models import Result

class EventEditForm(ModelForm):
    event_workers = ModelMultipleChoiceField(label = 'Работники события',
                            queryset=EventWorker.objects.filter(
                            is_active = True, data__modified = True,
                            data__user__is_active = True))
    class Meta:
        model = Event
        exclude = ['teachers',
                   'mentors',
                   'observers',
                   'is_private',
                   'is_payed',
                   'is_journey',
                   'is_active',
                   'has_journal'
                  ]

class EventForm(ModelForm):
    event_workers = ModelMultipleChoiceField(label = 'Работники события',
                            queryset=EventWorker.objects.filter(
                            is_active = True, data__modified = True,
                            data__user__is_active = True))

    
    class Meta:
        model = Event
        exclude = ['teachers',
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
