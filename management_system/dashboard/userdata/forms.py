# -*- coding: utf-8 -*-

from django.forms import ModelForm, RegexField, ChoiceField, Form
from dashboard.userdata.models import UserData, Passport, Zagran, BirthCert, OtherDoc

class UserDataForm(ModelForm):
	phone = RegexField(regex = r'^\+?1?\d{9,15}$', required = True,
					   error_message = ("Телефонный номер должен иметь формат +99999999999. Может содержать до 15 цифр"))
	class Meta:
		model = UserData
		exclude = ['user',
				   'modified',
				   ]

'''
Document type select form
'''
choices = (('P' , 'Паспорт'),
           ('Z', 'Загран. паспорт'),
           ('B', 'Свидетельство о рождении'),
           ('O', 'Другой документ'))

class DocumentTypeForm(Form):
    type = ChoiceField(label = 'Тип документa', choices = choices)
'''
end of document type select form
'''

class PassportForm(ModelForm):
    class Meta:
        model = Passport
        exclude = ['data']

class ZagranForm(ModelForm):
    class Meta:
        model = Zagran
        exclude = ['data']

class BirthCertForm(ModelForm):
    class Meta:
        model = BirthCert
        exclude = ['data']

class OtherDocForm(ModelForm):
    class Meta:
        model = OtherDoc
        exclude = ['data']
      
