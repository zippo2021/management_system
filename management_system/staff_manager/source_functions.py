from dashboard.userdata.models import UserData
from dashboard.event_worker.models import EventWorker
from dashboard.teacher.models import Teacher
from dashboard.mentor.models import Mentor
from dashboard.observer.models import Observer
from django.contrib.auth.models import User
from staff_manager.permissions import perms_to_classes

def create_staff_user(username, password, email = None,
					  perms = {
					  			'event_worker' : False,
								'teacher' : False,
								'mentor' : False,
								'observer' : False,
					  },
					  admin = False
					  ):

	#creating User
	user = User.objects.create_user(
		username = username
	)

	if email != None:
		user.email = email
	
	user.set_password(password)
	user.save()
	#creating userdata
	data = UserData(user = user)
	data.save()
	#creating additional data
	for key in perms_to_classes.keys():
		globals()[key] = globals()[perms_to_classes[key]](data = data)
		globals()[key].save()
	#setting permissions
	data.set_permissions(perms, admin)
	return user

def get_staff_members():
	staff = list(User.objects.filter(is_staff = True))
	for key in perms_to_classes.keys():
		staff = staff + [each.data.user for each in 
				globals()[perms_to_classes[key]].objects.all()]
	#c-style distinct() for lists
	return list(set(staff))
