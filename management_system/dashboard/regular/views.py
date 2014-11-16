from django.shortcuts import render, redirect
from dashboard.regular.models import RegularUser
from dashboard.regular.forms import RegularUserForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from decorators import should_have_regular_attr, should_be_regular, should_be_defined,should_be_staff
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.

@login_required
@should_have_regular_attr
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
def self_profile_view(request):
        base_data = request.user.UserData
        regular_data = request.user.UserData.RegularUser
        return render( request, 'self_regular_profile.html' , {'base_data' : base_data , 'regular_data' : regular_data })

@login_required
@should_be_staff
def regular_profile_view(request,uid):
        user = User.objects.get(id = uid)
        if hasattr(user.UserData, 'RegularUser'):
            base_data = user.UserData
            regular_data = user.UserData.RegularUser
            return render( request, 'regular_profile_view.html' , {'base_data' : base_data , 'regular_data' : regular_data })
        else:
            return render( request, 'regular_profile_view.html' , {})                                                  
                                     	

def regular_profile_view(request):
        data = request.user.UserData.RegularUser
        return render(request, 'regular_profile.html', {'user_data' : data})	



