from django.conf.urls import url
from events.events_manage import views

urlpatterns = [
	url(r'^main/(?P<eid>\d+)/$', views.main, name = 'events_manage_main'),
]
