from django.conf.urls import url
from dashboard.userdata import views

urlpatterns = [
	url(r'^edit', views.edit, name = 'edit_userdata'),
    url(r'^dialog_userdata_form', views.dialog_userdata, name = 'dialog_userdata_form'),
	url(r'^completed', views.completed, name = 'userdata_edited'),
    url(r'^base_profile_view', views.base_profile_view, name = 'base_profile_view'),
]
