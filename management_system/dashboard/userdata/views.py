from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from dashboard.userdata.forms import UserDataForm
from dashboard.userdata.models import UserData
from decorators import should_be_defined
from django.http import HttpResponse
# Create your views here.

@login_required
def tmp_base(request):
	return render(request, 'tmp_base.html', {})

@login_required
def edit(request):
    if request.method == 'POST':
		#userdata always exists if we passed should_have_data
		form = UserDataForm(request.POST, instance = request.user.UserData)
		#validate form and redirect
		if form.is_valid():
			user_data = form.save(commit = False)
			user_data.modified = True
			user_data.save()
			return render(request, 'userdata_completed.html', {})
    else:		
        form = UserDataForm(instance = request.user.UserData)

	return render(request, 'userdata_form.html', {'form' : form})
    

@login_required
@should_be_defined
def completed(request):
	return render(request, 'userdata_completed.html')

@login_required
@should_be_defined
def base_profile_view(request):
        base_data = request.user.UserData
        return render( request, 'base_profile.html' , {'base_data' : base_data})


