from django.conf.urls import url
from events.price_groups import views

urlpatterns = [
	url(r'^price_groups/add', views.add, name = 'price_group_add'),
    url(r'^price_groups/show', views.show, name = 'price_groups_show'),
   
]
