from django.forms import ModelForm
from events.events_admin.models import Event
class PriceChoice(ModelForm):
    class Meta:
        model = Event
        include = ['PriceGroup'
                  ]
