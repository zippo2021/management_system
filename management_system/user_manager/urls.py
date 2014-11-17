from django.conf.urls import url
from user_manager import views

urlpatterns = [
	url(r'^create', views.create, name = 'create_user'),
	url(r'^completed', views.completed, name = 'user_created'),
	url(r'^show_all', views.show_all, name = 'show_all_staff_members'),
	url(r'^edit_permissions/(?P<user_id>\d+)', views.edit_permissions,
		name = 'edit_user_permissions'),
	url(r'^deactivate/(?P<user_id>\d+)', views.deactivate,
		name = 'deactivate_user'),
]

