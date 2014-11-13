# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from staff_manager.forms import CreateStaffForm, EditPermissionsForm
from django.core.mail import send_mail
from staff_manager.source_functions import create_staff_user, get_staff_members
from base_source_functions import send_templated_email
from django.contrib.auth.models import User
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import user_passes_test
from permissions import perms_trans

@staff_member_required
def create(request):
	if request.method == 'POST':
		form = CreateStaffForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			#creating user
			perms = { each : cd[each] for each in perms_db.keys()}
			password = User.objects.make_random_password(length = 8)
			user = create_staff_user(username = cd['email'],
							  password = password,
					 		  email = cd['email'],
						  	  perms = perms,
							  admin = cd['admin']
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

@staff_member_required
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
		form = EditPermissionsForm(request.POST,
								   editor = request.user,
								   edited = user)
		if form.is_valid():
			cd = form.cleaned_data
			admin = cd.pop('admin')
			user.UserData.set_permissions(cd, admin)
			return redirect('show_all_staff_members')
	else:
		perms, admin = user.UserData.get_permissions()
		perms.update({'admin' : admin})
		form = EditPermissionsForm(initial = perms,
								   editor = request.user,
								   edited = user)
	return render(request,
				  'staff_manager_edit_permissions.html',
				  {'form' : form })

@user_passes_test(lambda u: u.is_superuser)
def deactivate(request, user_id):
	user = User.objects.get(id = user_id)
	user.is_active = not(user.is_active)
	user.save()
	return redirect('show_all_staff_members')
