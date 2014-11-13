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
from staff_manager.permissions import permissions_names

@receiver(user_activated)
def create_userdata_and_regular_user(**kwargs):
		user = kwargs['user']	
		data = UserData(user = user)
		data.save()
		regular = RegularUser(data = data)
		regular.save()
		user.save()

# Create your models here.
class UserData(models.Model):
	def get_permissions(self):
		perms = {each : getattr(self, 'is_' + each)
				for each in permissions_names}
		admin = self.user.is_staff
		return perms, admin
	
	def set_permissions(self, perms, admin):
		for each in permissions_names:
			setattr(self, 'is_' + each, perms[each])
		self.save()
		self.user.is_staff = admin
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
	
	is_event_worker = models.BooleanField(default = False)
	is_teacher = models.BooleanField(default = False)
	is_mentor = models.BooleanField(default = False)
	is_observer = models.BooleanField(default = False)
	modified = models.BooleanField(default = False)


admin.site.register(UserData)
