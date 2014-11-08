from django.shortcuts import render, redirect
from decorators import should_be_defined, should_be_undefined
from decorators import should_have_data, should_have_no_data
from django.contrib.auth.decorators import login_required
from dashboard.userdata.forms import UserDataForm
from dashboard.userdata.models import UserData
# Create your views here.

@login_required
@should_have_no_data
def create(request):
	if request.method == 'POST':
		form = UserDataForm(request.POST)
		if form.is_valid():
			user_data = form.save(commit = False)
			user_data.user = request.user
			user_data.save()
			return redirect('define_user_request')
	else:
		form = UserDataForm()
	return render(request, 'userdata_create.html', {'form' : form})

@login_required
@should_be_defined
def edit(request):
	if request.method == 'POST':
		#userdata always exists if we passed should_have_data
		form = UserDataForm(request.POST, instance = request.user.UserData)
		#validate form and redirect
		if form.is_valid():
			user_data = form.save()
			return redirect('userdata_edited')
	else:
		form = UserDataForm(instance = request.user.UserData)

	return render(request, 'userdata_edit.html', {'form' : form})

@login_required
@should_be_defined
def completed(request):
	return render(request, 'userdata_completed.html')

