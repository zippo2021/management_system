from django.conf.urls import url
from events.events_admin import views, forms

urlpatterns = [
    #test url: index
    url(r'^index', views.index, name = 'events_admin_index'),
    url(r'^add', views.event_wizard, name = 'add_event'),
    url(r'^completed', views.completed, name = 'event_added'),
    url(r'^show_all', views.show_all, name = 'show_all_events'),
    
]

