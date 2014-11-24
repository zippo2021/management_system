# -*- coding: utf-8 -*-

from django.forms import ModelForm, RegexField
from dashboard.regular.models import RegularUser
from django.core.exceptions import ValidationError 

class RegularUserForm(ModelForm):
	parent_1_phone = RegexField(regex = r'^\+?1?\d{9,15}$', label = "Телефон отца",
	                       		error_message = ("Телефонный номер должен иметь формат +99999999999. Может содержать до 15 цифр"))
	parent_2_phone = RegexField(regex = r'^\+?1?\d{9,15}$', label = "Телефон матери",
	                       		error_message = ("Телефонный номер должен иметь формат +99999999999. Может содержать до 15 цифр"))

	def clean(self):
		cd = super(RegularUserForm, self).clean()
		if not((cd['parent_1'] and cd['parent_1_phone']) or 
			   (cd['parent_2'] and cd['parent_2_phone'])):
			   raise ValidationError('Информация о хотя бы одном родителе должна бть заполнена', code = 'invalid' )
		else: return cd
	
	class Meta:
		model = RegularUser
		exclude = ['user','data', 'modified', 'is_active']
