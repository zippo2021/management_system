from django.db import models

# Create your models here.
class Observer(models.Model):
    data = models.OneToOneField('regular.UserData')

