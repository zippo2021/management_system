from django.forms import ModelForm
from define_user.models import DefineUserRequest

class DefineUserRequestForm(ModelForm):
	class Meta:
		model = DefineUserRequest
		exclude = ['user']
	
