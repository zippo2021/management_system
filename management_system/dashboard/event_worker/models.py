from django.db import models

# Create your models here.
class EventWorker(models.Model):
	data = models.OneToOneField('userdata.UserData',
								related_name = 'EventWorker')
	is_active = models.BooleanField(default = False)
