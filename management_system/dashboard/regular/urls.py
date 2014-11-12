from django.conf.urls import url
from dashboard.regular import views

urlpatterns = [
	url(r'^edit', views.edit, name = 'edit_regular'),
	url(r'^completed', views.completed, name = 'regular_edited'),
	url(r'^self_profile_view',views.self_profile_view, name = 'self_profile_view'),
    url(r'^regular_profile_view/(?P<uid>\d+)/$',views.regular_profile_view, name = 'regular_profile_view'),
]
