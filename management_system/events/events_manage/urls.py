from django.conf.urls import url
from events.events_manage import views

urlpatterns = [
	url(r'^main/(?P<event_id>\d+)/$', views.main, name = 'events_manage_main'),
    url(r'^edit_or_create_result/(?P<event_id>\d+)/(?P<user_id>\d+)',
        views.edit_or_create_result, name = 'edit_or_create_result'),
    url(r'^show/(?P<event_id>\d+)/(?P<role>\w+)/$', views.show_users, name = 'events_show_users'),
    url(r'^main/(?P<event_id>\d+)/(?P<uid>\d+)/(?P<role>\w+)/$', views.invite, name = 'event_invite'),
    url(r'^requests/(?P<event_id>\d+)/$', views.show_requests, name = 'events_show_requests'),
    url(r'^accept/(?P<request_id>\d+)/$', views.accept, name = 'events_accept_request'),
    url(r'^place_request/(?P<event_id>\d+)/$', views.place_request, name = 'place_request'),
    url(r'^decline_request/(?P<request_id>\d+)/$', views.decline_request, name = 'decline_request'),
    url(r'^request_completed/$', views.request_completed, name = 'request_completed'),
    url(r'^create_acceptance_email_template/(?P<event_id>\d+)/$', views.create_acceptance_email_template, name = 'create_acceptance_email_template'),
]

