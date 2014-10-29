from django.db import models

# Create your models here.
class EventWorker(models.Model):
    data = models.OneToOneField('regular.UserData')

