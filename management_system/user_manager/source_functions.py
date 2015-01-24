from dashboard.userdata.models import UserData, Admin
from dashboard.event_worker.models import EventWorker
from dashboard.teacher.models import Teacher
from dashboard.mentor.models import Mentor
from dashboard.observer.models import Observer
from django.contrib.auth.models import User
from user_manager.permissions import perms_to_classes

def create_user(username, password, email = None,
					  perms = {
					  			'event_worker' : False,
								'teacher' : False,
								'mentor' : False,
								'observer' : False,
								'regular' : False,
                                'admin' : False,
					  }):
	#creating User
	user = User.objects.create_user(
		username = username
	)

	if email != None:
		user.email = email
	
	user.set_password(password)
	user.save()
	
	#setting permissions
	user.UserData.set_permissions(perms)
	return user

def get_staff_members():
	staff = []
    #no regular users here
	staff_perms_list = perms_to_classes.keys()
	staff_perms_list.remove('regular')
	for key in staff_perms_list:
		staff = staff +\
		[each.data.user for each in globals()\
		[perms_to_classes[key]].objects.filter(is_active = True)]
	#c-style distinct() for lists
	return list(set(staff))
