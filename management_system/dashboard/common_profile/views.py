# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from dashboard.common_profile.source_functions import create_info
# Create your views here.

@login_required
def view_profile(request,uid):
    restr = True
    if request.user.UserData.id == int(uid):
        user = request.user.UserData
        edit_perm = True
        restr = False
    else:
        user = User.UserData.objects.get(id = uid)
        edit_perm = False
    base_data = user
 
    additional_data = create_info(request.user.UserData, user, restr)
    return render( request, 'view_profile.html' ,\
                   {'base_data' : base_data ,\
                   'additional_data' : additional_data,\
                   'edit_perm':edit_perm }
                 )

@login_required
def edit(request,role):
    if role == 'Teacher':
        url_role = 'teacher'
    if role == 'RegularUser':
        url_role = 'regular'
    
    return redirect('edit_'+url_role)
