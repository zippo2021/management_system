# -*- coding: utf-8 -*-

from django.forms import ModelForm, RegexField
from dashboard.userdata.models import UserData

class UserDataForm(ModelForm):
	phone = RegexField(regex = r'^\+?1?\d{9,15}$', required = True,
					   error_message = ("Телефонный номер должен иметь формат +99999999999. Может содержать до 15 цифр"))
	class Meta:
		model = UserData
		exclude = ['user', 'modified']
