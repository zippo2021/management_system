from django.db import models
from django.contrib.auth.models import User
'''
from ***.models import RegularUser, EventWorker, SubjectWorker, Mentor, Observer
'''

class Event(models.Model):
    name = models.CharField(verbose_name = 'Название', max_length = 100)
    comment = models.CharFielf(verbose_name = 'Комментарий',\
			       max_length = 1000, blank = True)
    place = models.CharField(verbose_name = 'Место проведения',\
			     max_length = 100)
    opened = models.DateField(verbose_name = 'Создано')
    closed = models.DateField(verbose_name = 'Закрыто')
    is_private = models.BooleanField()
    is_journey = models.BooleanField()
    is_payed = models.BooleanField()
	event_workers = models.ManyToManyField(EventWorker)
	subject_workers = models.ManyToManyField(SubjectWorker)
	mentors = models.ManyToManyField(Mentor)
    observers = models.ManyToManyField(Observer)
    
'''
group with number and it's participants
'''
class StudyGroup(models.Model):
    event = models.ForeignKey(Event)
    label = models.CharField(verbose_name = 'Название/Номер')
    users = models.ManyToManyField(RegularUser)



'''
price and participants applied for this price
'''
class PriceGroup(models.Model):
    event = models.ForeignKey(Event)
    price = models.IntegerField(verbose_name = 'Стоимость')
    users = models.ManyToManyField(RegularUser)
    
'''
Comments about user according to this event
'''
class PersonalComment(models.Model):
    event = models.ForeignKey(Event)
    user = models.ForeignKey(RegularUser)
    text = models.CharField(verbose_name = 'Комментарий', max_length = 1000)

'''
if event is a journey
'''
class JourneyData(models.Model):
    event = models.OneToOne(Event)
    tickets = models.ForeignKey(Ticket)
    departure_time = models.DateTimeField(verbose_name = 'Время отправления')
    info = models.CharField(verbose_name = 'Информация', blank = True)

class Ticket(models.Model)
    user = models.OneToOneField(RegularUser) ''' or any user? '''
    price = models.IntegerField(verbose_name = 'Цена билета', blank = True)
    place = nodels.CharField(verbose_name = 'Место', blank = True)
    is_apart = models.BooleanField()
'''
if event is private
'''
class Requests(models.Model):
    event = models.ForeignKey(Event)
    users = models.ManyToManyField(RegularUser)

class Contract(models.Model):
    event = models.ForeignKey(Event)
    user = models.ForeignKey(RegularUser)
    '''
    it has to be completed
    '''
