from dashboard.userdata.models import UserData
from dashboard.event_worker.models import EventWorker
from dashboard.teacher.models import Teacher
from dashboard.mentor.models import Mentor
from dashboard.observer.models import Observer
from django.contrib.auth.models import User


def create_staff_user(username, password, email = None,
					  perms = {
					  			'event_worker' : False,
								'teacher' : False,
								'mentor' : False,
								'observer' : False
					  },
					  admin = False):

	#creating User
	user = User.objects.create_user(
		username = username
	)

	if email != None:
		user.email = email
	
	user.set_password(password)
	user.is_sraff = admin
	user.save()
	#creating userdata
	data = UserData(user = user)
	data.save()
	#creating additional data
	if perms['event_worker']:
		event_worker = EventWorker(data = data)
		event_worker.save()
	if perms['teacher']:
		teacher = Teacher(data = data)
		teacher.save()
	if perms['mentor']:
		mentor = Mentor(data = data)
		mentor.save()
	if perms['observer']:
		observer = Observer(data = data)
		observer.save()
	return user

def get_staff_members():
	event_workers = [each.data.user for each in EventWorker.objects.all()]
	teachers = [each.data.user for each in Teacher.objects.all()]
	mentors = [each.data.user for each in Mentor.objects.all()]
	observers = [each.data.user for each in Observer.objects.all()]
	staff_members = {
					 'event_workers' : event_workers,
					 'teachers' : teachers,
					 'mentors' : mentors,
					 'observers' : observers
					}
	return staff_members
