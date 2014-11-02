# -*- coding: utf-8 -*-

from django.forms import ModelForm, ValidationError
from define_user.models import DefineUserRequest

class DefineUserRequestForm(ModelForm):
	def clean(self):
		cd = super(DefineUserRequestForm, self).clean()
		if not(cd['teacher'] or cd['observer']
			or cd['event_worker'] or cd['mentor']):
			raise ValidationError('Хотя бы одно поле должно быть выбрано')
		else: return cd
	class Meta:
		model = DefineUserRequest
		exclude = ['user']
	
