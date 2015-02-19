from django import forms
from events.events_admin.models import Event, Result
class PriceChoice(forms.Form):
    def __init__(self, *args, **kwargs):
        eid = kwargs.pop('event_id', None)
        super(PriceChoice, self).__init__(*args, **kwargs)        
        event = Event.objects.get(id = eid)
        self.fields['PriceGroup'] = forms.ModelChoiceField(queryset=event.PriceGroup.all())
    
class ResultForm(forms.ModelForm):
    class Meta:
        model = Result
        exclude = ['event', 'user']