# -*- coding: utf-8 -*-

from django.forms import Form, EmailField, BooleanField, HiddenInput
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from crispy_forms.helper import FormHelper, Layout
from crispy_forms.layout import Field, Fieldset, ButtonHolder, Submit

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
    #admin hidden has no label
    admin_hidden = BooleanField(required = False, label = '')
    use_admin_hidden = BooleanField(required = False, label = '')

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.layout = Layout(Fieldset(
                                    '',
                                    'regular',
                                    'observer',
                                    'mentor',
                                    'teacher',
                                    'event_worker',
                                    'admin'
                                    ),
                                    Field('admin_hidden', type="hidden"),
                                    Field('use_admin_hidden', type="hidden"),
                                  
        )
        editor = kwargs.pop('editor')
        edited = kwargs.pop('edited')
        super(EditPermissionsForm, self).__init__(*args, **kwargs)
        '''
        we always save admin state in hidden field
        '''
        #we should always hide this
        self.fields['admin_hidden'].widget.attrs['hidden'] = True
        self.fields['use_admin_hidden'].widget.attrs['hidden'] = True
        if 'initial' in kwargs.keys():
            initial = kwargs['initial']
            initial_admin = initial['admin']
            if not(editor.UserData.Admin.is_active) or\
                edited.UserData.Admin.is_superadmin:
                self.fields['admin'].widget.attrs['disabled'] = True
                self.fields['use_admin_hidden'].initial = True
            self.fields['admin_hidden'].initial = initial_admin
        '''
        whatever happens, we extract hidden field value to cleaned_data
        '''

    def clean(self):
        cleaned_data = super(EditPermissionsForm, self).clean()
        print cleaned_data
        if cleaned_data['use_admin_hidden']:
            print 'YES!'
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
