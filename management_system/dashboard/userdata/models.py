# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db import models
from django.contrib import admin
from django.dispatch import receiver
from registration.signals import user_activated
from dashboard.regular.models import RegularUser
from django.db.models.signals import post_save
from dashboard.event_worker.models import EventWorker
from dashboard.teacher.models import Teacher
from dashboard.mentor.models import Mentor
from dashboard.observer.models import Observer
from user_manager.permissions import perms_to_classes
from django.db.models.signals import post_save


# Create your models here.
class UserData(models.Model):
	def get_permissions(self):
		perms = {key : getattr(self, perms_to_classes[key]).is_active
				for key in perms_to_classes.keys()}
		return perms
	
	def set_permissions(self, perms):
		for key in perms_to_classes.keys():
			getattr(self, perms_to_classes[key]).is_active = perms[key]
			getattr(self, perms_to_classes[key]).save()
		self.user.save()
	
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

@receiver(post_save, sender = User)
def create_userdata(instance, created, **kwargs):
	if created:
		data = UserData(user = instance)
		data.save()

@receiver(user_activated)
def activate_regular_user(user, **kwargs):
	user.UserData.RegularUser.is_active = True
	user.UserData.RegularUser.save()

@receiver(post_save, sender = UserData)
def create_additional_data(instance, created, **kwargs):
	if created:
		for key in perms_to_classes.keys():
			globals()[key] = globals()[perms_to_classes[key]](data = instance)
			globals()[key].save()

class Admin(models.Model):
    data = models.OneToOneField(UserData, related_name = 'Admin')
    is_superadmin = models.BooleanField(default = False)
    is_active = models.BooleanField(default = False)

admin.site.register(Admin)

    
class OtherDoc(models.Model):
    user = models.OneToOneField(UserData, related_name = 'OtherDoc')
    type = models.CharField(verbose_name='Тип', max_length=255)
    ser = models.CharField(verbose_name='Серия',max_length=255)
    number = models.CharField(verbose_name='Номер',max_length=255)
    issued_by = models.CharField(verbose_name="Кем выдан",max_length=255,)
    when_issued = models.DateField(verbose_name="Когда выдан")
admin.site.register(OtherDoc)

class Passport(models.Model):
    user = models.OneToOneField(UserData, related_name='Passport')
    ser = models.PositiveIntegerField(verbose_name='Серия',max_length=4)
    number = models.PositiveIntegerField(verbose_name='Номер',max_length=6)
    issued_by = models.CharField(verbose_name="Кем выдан",max_length=255,)
    when_issued = models.DateField(verbose_name="Когда выдан")
    code = models.CharField(verbose_name="Код подразделения",max_length=30)
admin.site.register(Passport)

class BirthCert(models.Model):
    user = models.OneToOneField(UserData, related_name = 'BirthCert')
    ser = models.CharField(verbose_name='Серия',max_length=8)
    number = models.PositiveIntegerField(verbose_name='Номер',max_length=6)
    issued_by = models.CharField(verbose_name="Кем выдано",max_length=255)
    when_issued = models.DateField(verbose_name="Когда выдано")
admin.site.register(BirthCert)

class Zagran(models.Model):
    user = models.OneToOneField(UserData, related_name = 'Zagran')
    ser = models.PositiveIntegerField(verbose_name='Серия',max_length=2)
    number = models.PositiveIntegerField(verbose_name='Номер',max_length=7)
    issued_by = models.CharField(verbose_name="Кем выдан",max_length=255)
    when_issued = models.DateField(verbose_name="Когда выдан")
    exp_date = models.DateField(verbose_name="Срок действия")
admin.site.register(Zagran)

