from django.conf.urls import url

from define_user import views

urlpatterns = [
	url(r'^request', views.define_user_request, name = 'define_user_request'),
	url(r'^completed', views.define_user_completed, 
					   name = 'define_user_completed'),
]
