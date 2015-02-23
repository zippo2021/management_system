from django.conf.urls import url
from events.events_manage import views

urlpatterns = [
	url(r'^main/$', views.main,
                    name = 'events_manage_main'),
    url(r'^result/(?P<user_id>\d+)',
        views.edit_or_create_result,
                    name = 'events_manage_edit_or_create_result'),
    url(r'^choose/(?P<role>\w+)/$', views.choose_users,
                    name = 'events_manage_choose_users'),
    url(r'^invite/(?P<uid>\d+)/(?P<role>\w+)/$', views.invite,
                    name = 'events_manage_invite'),
    url(r'^requests', views.show_requests,
                    name = 'events_manage_show_requests'),
    url(r'^accept/(?P<request_id>\d+)/$', views.accept_request,
                    name = 'events_manage_accept_request'),
    url(r'^place_request', views.place_request, 
                    name = 'events_manage_place_request'),
    url(r'^decline_request/(?P<request_id>\d+)/$', views.decline_request,
                    name = 'events_manage_decline_request'),
    url(r'^email_template/acceptance', views.create_acceptance_email_template,
                    name = 'events_manage_create_acceptance_email_template'),
]

