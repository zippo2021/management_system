from django.db import models

# Create your models here.
class EventWorker(models.Model):
    def __unicode__ (self):
        return self.data.last_name +' '+ self.data.first_name
    
    data = models.OneToOneField('userdata.UserData',
								related_name = 'EventWorker')
    is_active = models.BooleanField(default = False)
