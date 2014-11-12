# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from staff_manager.forms import CreateStaffForm, EditPermissionsForm
from django.core.mail import send_mail
from staff_manager.source_functions import create_staff_user, get_staff_members
from base_source_functions import send_templated_email
from django.contrib.auth.models import User

def create(request):
	if request.method == 'POST':
		form = CreateStaffForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			#creating user
			perms = { each : cd[each] for each in
					  ('event_worker', 'teacher', 'mentor', 'observer')
			}
			password = User.objects.make_random_password(length = 8)
			user = create_staff_user(username = cd['email'],
							  password = password,
					 		  email = cd['email'],
						  	  perms = perms,
							  admin = cd['administrator']
			)
			#sending mail
			send_templated_email(subject = 'Создан аккаунт', 
				email_template_name = 'staff_manager_create_email.html',
				email_context = {'username' : user.username,
								 'password' : password,
								 'perms' : perms,
								 'admin' : user.is_staff
								 },
				recipients = user.email,
			)
			
			return redirect('staff_member_created')
		
	else:
		form = CreateStaffForm()
		
	return render(request, 'staff_manager_create.html', {'form' : form})

def completed(request):
	return render(request, 'staff_manager_completed.html')

def show_all(request):
	staff_members = get_staff_members()
	return render(request,
				  'staff_manager_show_all.html',
				  {'staff_members' : staff_members}
		   )

def edit_permissions(request, user_id):
	
	user = User.objects.get(id = user_id)
	if request.method == 'POST':
		form = EditPermissionsForm(request.POST)
		if form.is_valid():
			user.UserData.set_permissions(form.cleaned_data)
			return redirect('show_all_staff_members')
	else:
		perms = user.UserData.get_permissions()
		form = EditPermissionsForm(initial = perms)
	return render(request,
				  'staff_manager_edit_permissions.html',
				  {'form' : form })

