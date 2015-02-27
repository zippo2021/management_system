from django.conf.urls import url
from feedback import views

urlpatterns = [
	url(r'^send/$', views.send,
		name = 'feedback_send'),
]

