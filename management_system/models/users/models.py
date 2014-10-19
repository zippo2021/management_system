from django.db import models
from django.contrib.auth.models import User

class UserData(models.Model):
    user = models.OneToOneField(User)
    avatar = models.ImageField(verbose_name='Аватар',  upload_to='images/profile_pics',blank=True,null=True)
    first_name = models.CharField(verbose_name='Имя',  max_length=255)
    middle_name = models.CharField(verbose_name='Отчество',  max_length=255,blank=True, null=True)
    last_name = models.CharField(verbose_name='Фамилия',  max_length=255)
    phone  = models.CharField(verbose_name='Телефон',max_length=15,blank=True, null=True)

class EventWorker(models.Model):

class SubjectWorker(models.Model):

class Observer(models.Model):

class RegularUser(models.Model):
