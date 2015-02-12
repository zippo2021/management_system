from django.conf.urls import url
from events.events_manage import views

urlpatterns = [
	url(r'^main/(?P<eid>\d+)/$', views.main, name = 'events_manage_main'),
    url(r'^show/(?P<eid>\d+)/(?P<role>\w+)/$', views.show_users, name = 'events_show_users'),
    url(r'^main/(?P<eid>\d+)/(?P<uid>\d+)/(?P<role>\w+)/$', views.invite, name = 'event_invite'),
]
