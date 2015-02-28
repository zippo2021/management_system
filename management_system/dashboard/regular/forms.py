# -*- coding: utf-8 -*-

from django.core.exceptions import ValidationError
from django.forms import ModelForm, RegexField
from dashboard.regular.models import RegularUser
from django.core.exceptions import ValidationError 
from django.core.urlresolvers import reverse_lazy
from django.utils.safestring import mark_safe
from django.utils.translation import pgettext_lazy


class RegularUserForm(ModelForm):
	parent_1_phone = RegexField(regex = r'^\+?1?\d{9,15}$', label = "Телефон отца",
	                       		error_message = ("Телефонный номер должен иметь формат +99999999999. Может содержать до 15 цифр"))
	parent_2_phone = RegexField(regex = r'^\+?1?\d{9,15}$', label = "Телефон матери",
	                       		error_message = ("Телефонный номер должен иметь формат +99999999999. Может содержать до 15 цифр"))

	def clean(self):
		cd = super(RegularUserForm, self).clean()
		if not((cd['parent_1'] and cd['parent_1_phone']) or 
			   (cd['parent_2'] and cd['parent_2_phone'])):
			   raise ValidationError('Информация о хотя бы одном родителе должна быть заполнена', code = 'invalid' )
		else: return cd
	
	class Meta:
		model = RegularUser
		exclude = ['data', 'modified', 'is_active']
'''
!!!
Forms for Wizard
'''

class RegularUserFormStep1(ModelForm):

    class Meta:
        model = RegularUser
        fields = ('school', 'grad_date',)
        #help_texts = { 'school' : mark_safe('<a href=\'/schools/add\'>Добавить Школу</a>')}
        schools_add_url = '/schools/add/'
        help_texts = {'school':mark_safe("<a id='school_add' href = '#' onClick=\"ModalToggle('%s','%s','#form','Добавить школу',true); return false;\" >Добавить</a>" % (schools_add_url, schools_add_url))}

class RegularUserFormStep2(ModelForm):
    class Meta:
        model = RegularUser
        fields = ('country',
                  'city', 
                  'street', 
                  'building', 
                  'housing', 
                  'appartment',
                  'postal_code',)

class RegularUserFormStep3(ModelForm):
    #for some reason the fields below don't work !FIXIT!
    parent_1_phone = RegexField(regex = r'^\+?1?\d{9,15}$', label = "Телефон отца",
	                       		error_message = ("Телефонный номер должен иметь формат +99999999999. Может содержать до 15 цифр"), required = False)
    parent_2_phone = RegexField(regex = r'^\+?1?\d{9,15}$', label = "Телефон матери",
	                       		error_message = ("Телефонный номер должен иметь формат +99999999999. Может содержать до 15 цифр"), required = False)
     
    def clean(self):
		cd = super(RegularUserFormStep3, self).clean()
		if not(cd.get('parent_1') and cd.get('parent_1_phone') or 
			   cd.get('parent_2') and cd.get('parent_2_phone')):
			   raise ValidationError('Информация о хотя бы одном родителе должна быть заполнена', code = 'invalid' )
		return cd
    
    class Meta:
        model = RegularUser
        fields = ('birthdate',
                  'birthplace',
                  'parent_1',
                  'parent_1_phone',
                  'parent_2',
                  'parent_2_phone',)

