#-*- coding: utf-8 *-*
from django import forms
from events.events_admin.models import Event, Result, AcceptanceEmailTemplate

class PriceChoiceForm(forms.Form):
    def __init__(self, *args, **kwargs):
        eid = kwargs.pop('event_id', None)
        super(PriceChoiceForm, self).__init__(*args, **kwargs)        
        event = Event.objects.get(id = eid)
        self.fields['price_group'] = forms.ModelChoiceField(queryset=event.PriceGroup.all())
    
class ResultForm(forms.ModelForm):
    class Meta:
        model = Result
        exclude = ['event', 'user']

class AcceptanceEmailTemplateForm(forms.ModelForm):
    class Meta:
        model = AcceptanceEmailTemplate
        exclude = ['event']
