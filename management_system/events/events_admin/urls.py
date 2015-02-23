from django.conf.urls import url
from events.events_admin import views, forms

urlpatterns = [
    url(r'^add', views.event_wizard, name = 'events_admin_event_wizard'),
    url(r'^show_all', views.show_all, name = 'events_admin_show_all'),
    url(r'^edit/(?P<event_id>\d+)/(?P<base_or_journey>\w+)',
        views.edit, name = 'events_admin_edit'),
    url(r'^deactivate/(?P<event_id>\d+)', views.deactivate,
        name = 'events_admin_deactivate'),
]

