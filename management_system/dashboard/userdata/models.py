# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db import models
from django.contrib import admin
from django.dispatch import receiver
from registration.signals import user_activated
from dashboard.regular.models import RegularUser
from django.db.models.signals import post_save

#activation signal
#@receiver(post_save, sender = User)
@receiver(user_activated)
def create_userdata_and_regular_user(**kwargs):
#def create_userdata_and_regular_user(sender, instance, created, **kwargs):
#	if created:
		data = UserData(user = kwargs['user'])
		data.save()
		regular = RegularUser(data = data)
		regular.save()

# Create your models here.
class UserData(models.Model):
	def __str__ (self):
		return self.user.__str__()
	
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
	
	modified = models.BooleanField(default = False)


admin.site.register(UserData)
