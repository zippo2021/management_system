from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

# Create your views here.

@login_required
def view_profile(request,uid):
    no_restr = False
    if request.user.id == int(uid):
        user = request.user
        edit_perm = True
        no_restr = True
    else:
        user = User.objects.get(id = uid)
        edit_perm = False
    
    base_data = user.UserData
    additional_data = {}
    if user.UserData.Teacher.is_active:
        additional_data['teacher_data'] = user.UserData.Teacher
    if user.UserData.RegularUser.is_active:
        additional_data['regular_data'] = user.UserData.RegularUser
    if user.UserData.Mentor.is_active:
        additional_data['mentor_data'] = user.UserData.Mentor
    if user.UserData.Observer.is_active:
        additional_data['observer_data'] = user.UserData.Observer
    
    return render( request, 'view_profile.html' , {'base_data' : base_data , 'additional_data' : additional_data, 'edit_perm':edit_perm })
