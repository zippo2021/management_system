from django.conf.urls import url
from staff_manager import views

urlpatterns = [
	url(r'^create', views.create, name = 'create_staff_member'),
	url(r'^completed', views.completed, name = 'staff_member_created'),
	url(r'^show_all', views.show_all, name = 'show_all_staff_members'),
	url(r'^edit_permissions/(?P<user_id>\d+)', views.edit_permissions,
		name = 'edit_staff_member_permissions'),
	url(r'^deactivate/(?P<user_id>\d+)', views.deactivate,
		name = 'deactivate_staff_member')
]

