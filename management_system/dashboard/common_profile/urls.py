from django.conf.urls import url
from dashboard.common_profile import views

urlpatterns = [
    url(r'^view/(?P<uid>\d+)/$', views.view_profile,
                            name = 'common_profile_view_profile'),
    url(r'^edit/parse/(?P<role>\w+)/$', views.edit,
                            name = 'common_profile_edit')
]
