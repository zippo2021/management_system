# -*- coding: utf-8 -*-

from django.forms import Form, EmailField, BooleanField
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class CreateStaffForm(Form):
	email = EmailField(required = True)
	event_worker = BooleanField(required = False)
	teacher = BooleanField(required = False)
	mentor = BooleanField(required = False)
	observer = BooleanField(required = False)
	administrator = BooleanField(required = False)

	def clean(self):
		cd = super(CreateStaffForm, self).clean()
		if not(cd['event_worker'] or cd['teacher']
		   or cd['mentor'] or cd['observer'] or cd['administrator']):
				raise ValidationError('Не выбрано ни одного поля!',
									  code = 'Invalid')
		else:
				return cd

	def clean_email(self):
		email = self.cleaned_data['email']
		if User.objects.filter(email = email).exists():
			raise ValidationError('Пользователь с таким e-mail уже существет',
								  code = 'Invalid email')
		else:
			return email

class EditPermissionsForm(Form):
	def __init__(self, *args, **kwargs):
		super(EditPermissionsForm, self).__init__(*args, **kwargs)
		if self.initial:	
			current_perms = self.initial
			for key in current_perms.keys():
				if current_perms[key]:
					self.fields[key].widget.attrs['disabled'] = 'disabled'
				
	event_worker = BooleanField(required = False)
	teacher = BooleanField(required = False)
	mentor = BooleanField(required = False)
	observer = BooleanField(required = False)
	administrator = BooleanField(required = False)
