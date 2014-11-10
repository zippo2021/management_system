from django.conf.urls import url
from dashboard.regular import views

urlpatterns = [
	url(r'^edit', views.edit, name = 'edit_regular'),
	url(r'^completed', views.completed, name = 'regular_edited'),
	url(r'^regular_profile_view',views.regular_profile_view, name = 'regular_profile_view'),
]
