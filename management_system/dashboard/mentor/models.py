from django.db import models

# Create your models here.
class Mentor(models.Model):
    data = models.OneToOneField('regular.UserData')

