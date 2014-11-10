from django.conf.urls import url

from define_user import views

urlpatterns = [
	url(r'^request', views.request, name = 'define_user_request'),
	url(r'^completed', views.completed, 
					   name = 'define_user_completed'),
	url(r'^show_requests', views.show_requests,
					   name = 'define_user_show_requests'),
	url(r'^apply/(?P<define_user_request_id>[0-9]+)', 
					   views.apply_request, name = 'define_user_apply'),
    url(r'^define_regular', views.define_regular, name = 'define_regular'),
]
