# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect
from user_manager.forms import CreateUserForm, EditPermissionsForm
from decorators import should_be_admin
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from user_manager.source_functions import create_user, get_staff_members
from base_source_functions import send_templated_email
from django.contrib.auth.models import User
from django.http import HttpResponse
from user_manager.permissions import perms_to_classes, perms_to_language
from dashboard.common_profile.source_functions import perms_to_list

@login_required
@should_be_admin
def create(request):
	if request.method == 'POST':
		form = CreateUserForm(request.POST)
		if form.is_valid():
			#creating user
			perms = { each : form.cleaned_data[each] 
					  for each in perms_to_classes.keys()}

			password = User.objects.make_random_password(length = 8)
			user = create_user(username = form.cleaned_data['email'],
							  password = password,
					 		  email = form.cleaned_data['email'],
						  	  perms = perms,
			)
			#sending mail
			send_templated_email(subject = 'Создан аккаунт', 
				email_template_name = 'user_manager_create_email.html',
				email_context = {'username' : user.username,
								 'password' : password,
								 'perms' : perms_to_list(perms),
								 'admin' : user.is_staff,
                                 'perms_to_language' : perms_to_language,
								 },
				recipients = user.email,
			)
			status = "success"
			return HttpResponse(status)
		
	else:
		form = CreateUserForm()
		
	return render(request, 'user_manager_create.html', {'form' : form})

@login_required
@should_be_admin
def show_all(request):
	staff_members = get_staff_members()
	return render(request,
				  'user_manager_show_all.html',
				  {'staff_members' : staff_members}
		   )
		   
@login_required
@should_be_admin
def edit_permissions(request, user_id):
	user = User.objects.get(id = user_id)
	if request.method == 'POST':
		form = EditPermissionsForm(request.POST,
								   editor = request.user,
								   edited = user)
		if form.is_valid():
			cleaned_data = form.cleaned_data
			#set new permissions
			user.UserData.set_permissions(cleaned_data)
			status = "success"
			return HttpResponse(status)
	else:
		#load permissions to form
		perms = user.UserData.get_permissions()
		form = EditPermissionsForm(initial = perms,
								   editor = request.user,
								   edited = user)
	return render(request,
				  'user_manager_edit_permissions.html',
				  {'form' : form })

@login_required
@should_be_admin
def deactivate(request, user_id):
    user = User.objects.get(id = user_id)
    #we can not deactivate superadmin
    if not(user.UserData.Admin.is_superadmin):
        user.is_active = not(user.is_active)
        user.save()
    else: pass #FIXME
    return redirect('user_manager_show_all')
