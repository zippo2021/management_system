from django.db import models

# Create your models here.
class Mentor(models.Model):
	data = models.OneToOneField('userdata.UserData', related_name = 'Mentor')
	is_active = models.BooleanField(default = False)

