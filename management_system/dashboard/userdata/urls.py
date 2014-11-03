from django.conf.urls import url
from dashboard.userdata import views

urlpatterns = [
	url(r'^change', views.change, name = 'change_userdata'),
	url(r'^completed', views.completed, name = 'userdata_changed'),
]
