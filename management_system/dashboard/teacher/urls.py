from django.conf.urls import url
from dashboard.teacher import views

urlpatterns = [
	url(r'^edit/teacher', views.edit, name = 'teacher_edit'),
]
