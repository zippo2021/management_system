# -*- coding: utf-8 -*-

from django.forms import Form, EmailField, BooleanField
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class StaffForm(Form):
	event_worker = BooleanField(required = False)
	teacher = BooleanField(required = False)
	mentor = BooleanField(required = False)
	observer = BooleanField(required = False)
	admin = BooleanField(required = False)

class EditPermissionsForm(StaffForm):
	def __init__(self, *args, **kwargs):
		editor = kwargs.pop('editor')
		edited = kwargs.pop('edited')
		super(EditPermissionsForm, self).__init__(*args, **kwargs)
		if not(editor.is_superuser) or edited.is_superuser:
			self.fields['admin'].widget.attrs['disabled'] = 'disabled'
			

class CreateStaffForm(StaffForm):
	email = EmailField(required = True)

	def clean(self):
		cd = super(CreateStaffForm, self).clean()
		if not(cd['event_worker'] or cd['teacher']
		   or cd['mentor'] or cd['observer'] or cd['admin']):
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


