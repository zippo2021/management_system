from django.conf.urls import url
from events.events_manage import views

urlpatterns = [
	url(r'^main/(?P<eid>\d+)/$', views.main, name = 'events_manage_main'),
    url(r'^edit_or_create_result/(?P<event_id>\d+)/(?P<user_id>\d+)',
        views.edit_or_create_result, name = 'edit_or_create_result'),
    url(r'^show/(?P<eid>\d+)/(?P<role>\w+)/$', views.show_users, name = 'events_show_users'),
    url(r'^main/(?P<eid>\d+)/(?P<uid>\d+)/(?P<role>\w+)/$', views.invite, name = 'event_invite'),
    url(r'^requests/(?P<eid>\d+)/$', views.show_requests, name = 'events_show_requests'),
    url(r'^accept/(?P<eid>\d+)/(?P<uid>\d+)/$', views.accept, name = 'events_accept_request'),
    url(r'^place_request/(?P<eid>\d+)/$', views.place_request, name = 'place_request'),
    url(r'^deny_request/(?P<eid>\d+)/(?P<uid>\d+)/$', views.deny_request, name = 'deny_request'),
    url(r'^request_completed/(?P<eid>\d+)/$', views.request_completed, name = 'request_completed'),
]
