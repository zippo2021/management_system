# -*- coding: utf-8 -*-

from django.forms import Form, EmailField, BooleanField, HiddenInput
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class UserForm(Form):
	regular = BooleanField(required = False, label = "Ученик")
	event_worker = BooleanField(required = False,
								label = "Управляющий событиями")
	teacher = BooleanField(required = False, label = "Учитель")
	mentor = BooleanField(required = False, label = "Воспитатель")
	observer = BooleanField(required = False, label = "Наблюдатель")
	admin = BooleanField(required = False, label = "Администратор")

	def clean(self):
		cleaned_data = super(UserForm, self).clean()
		even_one_selected = False
		for key in cleaned_data.keys():
			even_one_selected = even_one_selected or cleaned_data[key]
		if not(even_one_selected):
			raise ValidationError('Не выбрано ни одного поля!',
									  code = 'Invalid')
		else:
			return cleaned_data


class EditPermissionsForm(UserForm):
	admin_hidden = BooleanField(required = False, widget = HiddenInput())
	
	def __init__(self, *args, **kwargs):
		editor = kwargs.pop('editor')
		edited = kwargs.pop('edited')
		super(EditPermissionsForm, self).__init__(*args, **kwargs)
		'''
		condition:
		if someone tries to edit permissions, but he is not able
		to edit admin status, then this hides admin field and
		saves current admin status in hidden field
		'''
		if 'initial' in kwargs.keys():
			initial = kwargs['initial']
			initial_admin = initial['admin']
			if not(editor.is_superuser) or edited.is_superuser:
				self.fields['admin'].widget.attrs['disabled'] = True
				self.fields['admin_hidden'].initial = initial_admin
		'''
		and now if condition* happend we extract hidden field's value to
		cleaned data normal field value.
		This way view has no need to think about what happend. It works
		with this form as if there wasn't any hidden field
		'''
	def clean(self):
		cleaned_data = super(EditPermissionsForm, self).clean()
		if not(hasattr(cleaned_data, 'admin')):
			cleaned_data['admin'] = cleaned_data.pop('admin_hidden')
			return cleaned_data

class CreateUserForm(UserForm):
	email = EmailField(required = True, label = "e-mail")

	def clean_email(self):
		email = self.cleaned_data['email']
		if User.objects.filter(email = email).exists():
			raise ValidationError('Пользователь с таким e-mail уже существет',
								  code = 'Invalid email')
		else:
			return email
