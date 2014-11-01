from django.shortcuts import render, redirect
from define_user.forms import DefineUserRequestForm
from define_user.models import DefineUserRequest
# Create your views here.
def define_user_request(request):
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
			form = DefineUserRequestForm(request.user.DefineUserRequest)
	
	return render(request, 'define_user_request.html', {'form' : form})

def define_user_completed(request):
	define_request = request.user.DefineUserRequest
	return render(request, 'define_user_completed.html', 
						  {'define_request': define_request})
