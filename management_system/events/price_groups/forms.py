
from django.forms import ModelForm
from events.price_groups.models import PriceGroup

class PriceGroupForm(ModelForm):
    class Meta:
        model = PriceGroup
        exclude = ['event',
                   'users',
                   ]
