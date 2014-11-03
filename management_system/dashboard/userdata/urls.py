from django.conf.urls import url
from dashboard.userdata import views

urlpatterns = [
	url(r'^edit', views.edit, name = 'edit_userdata'),
	url(r'^create', views.create, name = 'create_userdata'),
	url(r'^completed', views.completed, name = 'userdata_changed'),
]
