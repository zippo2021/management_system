from django.conf.urls import url
from dashboard.regular import views, forms

urlpatterns = [
	url(r'^edit', views.regular_user_wizard, name = 'edit_regular'),
	url(r'^completed', views.completed, name = 'regular_edited'),
	
]
