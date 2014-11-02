from django.shortcuts import render, redirect
from define_user.forms import DefineUserRequestForm
from define_user.models import DefineUserRequest
from dashboard.regular.models import UserData
from dashboard.teacher.models import Teacher
from dashboard.mentor.models import Mentor
from dashboard.event_worker.models import EventWorker
from dashboard.observer.models import Observer
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
# Create your views here.
@login_required
def request(request):
	if request.method == 'POST':
		#update eisting data, if exists
		if hasattr(request.user, 'DefineUserRequest'):
			form = DefineUserRequestForm(request.POST, 
				   instance = request.user.DefineUserRequest)
		else:
			form = DefineUserRequestForm(request.POST)
		#validate form and redirect
		if form.is_valid():
			define_request = form.save(commit = False)
			define_request.user = request.user
			define_request.save()
			return redirect('define_user_completed')
	
	else:
		#fill new form with existing data, if exists
		if hasattr(request.user, 'DefineUserRequest'):
			form = DefineUserRequestForm(
						instance = request.user.DefineUserRequest
			)
		else:
			form = DefineUserRequestForm()
	
	return render(request, 'request.html', {'form' : form})

@login_required
def completed(request):
	define_request = request.user.DefineUserRequest
	return render(request, 'completed.html', 
						  {'define_request': define_request})

@staff_member_required
def show_requests(request):
	requests = DefineUserRequest.objects.all()
	return render(request, 'show_requests.html', {'requests' : requests})

@staff_member_required
def apply_request(request, define_user_request_id):
	define_request = DefineUserRequest.objects.get(id = define_user_request_id)
	user = define_request.user
	user.UserData = UserData()
	if define_request.teacher:
		user.UserData.Teacher = Teacher()
	if define_request.event_worker:
		user.UserData.EventWorker = EventWorker()
	if define_request.mentor:
		user.UserData.Mentor = Mentor()
	if define_request.observer:
		user.UserData.Observer = Observer()
	user.DefineUserRequest.delete()
	return redirect('define_user_show_requests');
