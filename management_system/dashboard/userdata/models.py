# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class UserData(models.Model):
    user = models.OneToOneField(User, related_name = 'UserData')
    avatar = models.ImageField(
                    verbose_name = 'Аватар',
                    upload_to ='images/profile_pics',
                    blank = True,
                    null = True,
    )

    first_name = models.CharField(verbose_name = 'Имя', max_length = 255)

    middle_name = models.CharField(
                    verbose_name = 'Отчество',
                    max_length = 255,
                    blank = True,
                    null = True,
    )
    
    last_name = models.CharField(verbose_name = 'Фамилия',  max_length = 255)
    
    phone  = models.CharField(
                    verbose_name = 'Телефон',
                    max_length = 15,
                    null = True,
    )

