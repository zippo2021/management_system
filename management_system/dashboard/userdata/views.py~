from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from dashboard.userdata.forms import UserDataForm
from dashboard.userdata.models import UserData
from decorators import should_be_defined
# Create your views here.

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
			return redirect('userdata_edited')
	else:
		form = UserDataForm(instance = request.user.UserData)

	return render(request, 'userdata_edit.html', {'form' : form})

@login_required
@should_be_defined
def completed(request):
	return render(request, 'userdata_completed.html')

