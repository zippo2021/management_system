# -*- coding: utf-8 -*-

from django.forms import FileInput,ImageField,ModelForm, RegexField, ChoiceField, Form
from dashboard.userdata.models import UserData, Passport, Zagran, BirthCert, OtherDoc

class UserDataForm(ModelForm):
        avatar = ImageField(label='Аватар',required=False, error_messages = {'invalid':"Только изображения"}, widget=FileInput)
	phone = RegexField(regex = r'^\+?1?\d{9,15}$', required = True,
      					   error_message = ("Телефонный номер должен иметь формат +99999999999. Может содержать до 15 цифр"))
	class Meta:
		model = UserData
		exclude = ['user',
                           'modified',
                ]
        def clean_avatar(self):
                # получаем данные из нужного поля
                  picture =  self.cleaned_data['avatar']
                  if picture:
                      try:
                      # првряем размеры изображения
                      # получаем размеры загружаемого изображения
                          w, h = get_image_dimensions(picture)
                      # задаем ограничения размеров
                          max_width = 200 
                          max_height = 300 
                      # собственно сравнение
                          if w > max_width or h > max_height:
                              raise forms.ValidationError(u'Максимальный размер изображения %s x %s пикселов.' % (max_height, max_width))
                      # не пропускаем файлы, размер (вес) которых более 100 килобайт
                          if len(picture) > (500 * 1024):
                              raise forms.ValidationError(u'Размер изображения не может превышать 500 кб.')
                      except AttributeError:
                          pass
                      return picture
    
'''
Documeent type select form
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
        exclude = ['user']

class ZagranForm(ModelForm):
    class Meta:
        model = Zagran
        exclude = ['user']

class BirthCertForm(ModelForm):
    class Meta:
        model = BirthCert
        exclude = ['user']

class OtherDocForm(ModelForm):
    class Meta:
        model = OtherDoc
        exclude = ['user']
      
