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
from permissions import perms_trans

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
	def get_permissions(self):
		perms = {key : hasattr(self, perms_trans[key]) 
				for key in perms_trans.keys()}
		perms['administrator'] = self.user.is_staff
		return perms
	
	def set_permissions(self, perms):
		old_perms = self.get_permissions()
		to_set = [key for key in perms.keys()
				  if perms[key] and not(old_perms[key])]
		if 'administrator' in to_set:
			self.user.is_staff = True
			self.user.save()
			to_set.remove('administrator')
		for each in to_set:
			globals()[each] = globals()[perms_trans[each]](data = self)
			globals()[perms_trans[each]].save()

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
