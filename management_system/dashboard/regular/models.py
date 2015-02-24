# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin

class RegularUser(models.Model):
    def __unicode__ (self):
        return self.data.last_name +' '+ self.data.first_name
    data = models.OneToOneField('userdata.UserData',
   								related_name = 'RegularUser',
                                blank = True,
    )
	
    grad_date = models.CharField(verbose_name = 'Год окончания школы',
								 max_length=4, 
    )
	
    birthdate = models.DateField(verbose_name = 'Дата рождения', null = True)
	
    birthplace = models.CharField(
                    verbose_name = 'Место рождения',
                    max_length = 255,
    )
	
    postal_code = models.CharField(
                    verbose_name = 'Почтовый индекс',
                    max_length=6,
    )
	
    country = models.CharField(verbose_name = 'Страна', max_length = 30)
    city = models.CharField(verbose_name = 'Город', max_length = 255)
    street = models.CharField(verbose_name='Улица',
                              max_length = 255,
                              blank = True,
                              default = '')
	
    building = models.CharField(
                    verbose_name = 'Дом',  
                    max_length = 4,
                    blank = True,
                    default = ''
    )
	
    housing = models.CharField(verbose_name = 'Корпус',  max_length = 2, blank = True)
    appartment = models.CharField(verbose_name = 'Квартира',  max_length = 5, blank = True)
    parent_1 = models.CharField(verbose_name = 'ФИО отца',
								max_length = 255,
								blank = True,
                                default = ''
    )
    parent_1_phone  = models.CharField(verbose_name = 'Телефон отца',
									   max_length = 15,
									   blank = True,
                                       default = ''
    )
	
    parent_2 = models.CharField(
                    verbose_name = 'ФИО матери', 
                    max_length = 255,
                    blank = True,
                    default = ''
    )
	
    parent_2_phone = models.CharField(
                    verbose_name = 'Телефон матери',
                    max_length = 15, 
                    blank = True,
                    default = ''
    )
	
    school = models.ForeignKey('schools.School',
                               related_name = 'RegularUser',
                               verbose_name = 'Школа',
                               null = True,)

    modified = models.BooleanField(default = False)
    is_active = models.BooleanField(default = False)

admin.site.register(RegularUser)
