from django.conf.urls import url
from events.price_groups import views

urlpatterns = [
	url(r'^main/(?P<eid>\d+)/$', views.add, name = 'price_group_add'),
    url(r'^show/(?P<eid>\d+)/$', views.show, name = 'price_groups_show'),
   
]