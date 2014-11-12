from django.conf.urls import url
from dashboard.teacher import views

urlpatterns = [
	url(r'^edit', views.edit, name = 'edit_teacher'),
	url(r'^completed', views.completed, name = 'teacher_edited'),
    url(r'^self_profile_view',views.self_profile_view, name = 'self_profile_view'),
]
