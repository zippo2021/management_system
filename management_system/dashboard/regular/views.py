from django.shortcuts import render, redirect
from dashboard.regular.models import RegularUser
from dashboard.regular.forms import RegularUserForm
from django.contrib.auth.decorators import login_required
from decorators import should_be_regular_possibly_unfilled, should_be_regular

# Create your views here.

@login_required
@should_be_regular_possibly_unfilled
def edit(request):
	if request.method == 'POST':
		form = RegularUserForm(request.POST,
			   instance = request.user.UserData.RegularUser)
		if form.is_valid():
			regular = form.save(commit = False)
			regular.modified = True
			regular.save()
			return redirect('regular_edited')
	else:
		form = RegularUserForm(instance = request.user.UserData.RegularUser)
	
	return render(request, 'regular_edit.html', {'form' : form})

@login_required
@should_be_regular
def completed(request):
	return render(request, 'regular_completed.html')

@login_required
@should_be_regular
def regular_profile_view(request):
        data = request.user.UserData.RegularUser
        return render(request, 'regular_profile.html', {'user_data' : data})	


