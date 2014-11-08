from django.shortcuts import render, redirect
from decorators import should_be_teacher
from django.contrib.auth.decorators import login_required
from dashboard.teacher.forms import TeacherForm
from dashboard.teacher.models import Teacher
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
