from django.conf.urls import url
from dashboard.common_profile import views

urlpatterns = [
    url(r'^view_profile/(?P<uid>\d+)/$', views.view_profile, name = 'view_profile'),
    url(r'^view_profile/(?P<role>\w+)/$', views.edit, name = 'edit_common'),
]
