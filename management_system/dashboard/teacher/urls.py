from django.conf.urls import url
from dashboard.teacher import views

urlpatterns = [
	url(r'^edit', views.edit, name = 'teacher_edit'),
]
