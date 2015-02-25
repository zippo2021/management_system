from django.conf.urls import url
from events.price_groups import views

urlpatterns = [
	url(r'^price_groups/add', views.add, name = 'price_groups_add'),
]
