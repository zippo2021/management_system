from django.conf.urls import url
from user_manager import views

urlpatterns = [
    url(r'^add', views.create, name = 'user_manager_create'),
	url(r'^show_staff', views.show_all, name = 'user_manager_show_all'),
	url(r'^edit_permissions/(?P<user_id>\d+)', views.edit_permissions,
		name = 'user_manager_edit_permissions'),
	url(r'^deactivate/(?P<user_id>\d+)', views.deactivate,
		name = 'user_manager_deactivate'),
]

