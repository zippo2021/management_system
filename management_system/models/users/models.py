from django.db import models
from django.contrib.auth.models import User

'''
from event.models import Event
'''

class UserData(models.Model):
    user = models.OneToOneField(User)
    
	avatar = models.ImageField(verbose_name = 'Аватар',\
			   		       	   upload_to ='images/profile_pics',\
							   blank = True, null = True)
    
	first_name = models.CharField(verbose_name = 'Имя', max_length = 255)
    
	middle_name = models.CharField(verbose_name = 'Отчество',\
								   max_length = 255, blank = True, null = True)
    
	last_name = models.CharField(verbose_name = 'Фамилия',  max_length = 255)
    
	phone  = models.CharField(verbose_name = 'Телефон', \
							  max_length = 15,blank = True, null = True)

	is_regular_user = models.BooleanField()
	is_event_worker = models.BooleanField()
	is_subject_worker = models.BooleanField()
	is_observer = models.BooleanField()

class EventWorker(models.Model):
	data = models.OneToOneField(UserData)

class SubjectWorker(models.Model):
	data = models.OneToOneField(UserData)
	subject = models.CharField(verbose_name = 'Предмет', max_length = 100)

class Observer(models.Model):
	data = models.OneToOneField(UserData)

class RegularUser(models.Model):
	data = models.OneToOneField(UserData)

	grad_date = models.CharField(verbose_name = 'Год окончания школы',\
								 max_length = 4, null = True)

    birthdate = models.DateField(verbose_name = 'Дата рождения',null = True)

	birthplace = models.CharField(verbose_name = 'Место рождения',\
								  max_length = 255)

	postal_code = models.CharField(verbose_name = 'Почтовый индекс',\
								   max_length=6)

	country = models.CharField(verbose_name = 'Страна', max_length = 30)
	city = models.CharField(verbose_name = 'Город', max_length = 255)
	street = models.CharField(verbose_name='Улица', max_length = 255) 

	building = models.CharField(verbose_name = 'Дом',  max_length = 4,\
								null = True, blank = True)

	housing = models.CharField(verbose_name = 'Корпус',  max_length = 2)
	appartment = models.CharField(verbose_name = 'Квартира',  max_length = 5)
	parent_1 = models.CharField(verbose_name = 'ФИО отца',  max_length = 255)
	
	parent_1_phone  = models.CharField(verbose_name = 'Телефон отца',\
									   max_length = 15)

	parent_2 = models.CharField(verbose_name = 'ФИО матери', max_length = 255,\
								blank = True, null = True)

	parent_2_phone = models.CharField(verbose_name = 'Телефон матери',\
									  max_length = 15, blank = True,\
									  null = True)

	school = models.ForeignKey(School)
	notes = models.ForeignKey(Note)

class Note(models.Model)
	author = models.ForeignKey(SubjectWorker)
	receiver = models.ForeignKey(RegularUser)
	text = models.CharField(verbose_name = 'Запись', max_length = 1000)

class School(models.Model)
	name = models.CharField(verbose_name = 'Название', max_length = 100)
	country = models.CharField(verbose_name = 'Страна', max_length = 30)
	city = models.CharField(verbose_name = 'Город', max_length = 30)

