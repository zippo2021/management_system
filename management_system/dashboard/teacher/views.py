from django.shortcuts import render, redirect
from decorators import should_be_teacher
from django.contrib.auth.decorators import login_required
from dashboard.teacher.forms import TeacherForm
from dashboard.teacher.models import Teacher
from django.contrib.auth.models import User

# Create your views here.

@login_required
@should_be_teacher
def edit(request):
	if request.method == 'POST':
		form = TeacherForm(request.POST,
			   instance = request.user.UserData.Teacher)
		if form.is_valid():
			teacher = form.save()
			return redirect ('teacher_edited')
	else:
		form = TeacherForm(instance = request.user.UserData.Teacher)
	return render(request, 'teacher_edit.html', {'form' : form})

@login_required
@should_be_teacher
def completed(request):
	return render(request, 'teacher_completed.html')

@login_required
def profile_view(request,uid):
        if request.user.id == int(uid):
            user = request.user
            edit_perm = True
        else:
            user = User.objects.get(id = uid)
            edit_perm = False
        base_data = user.UserData
        teacher_data = user.UserData.Teacher
        
        return render( request, 'teacher_profile_view.html' , {'base_data' : base_data , 'additional_data' : teacher_data, 'edit_perm':edit_perm })
