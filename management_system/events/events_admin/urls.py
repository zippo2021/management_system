from django.conf.urls import url
from events.events_admin import views, forms

urlpatterns = [
    url(r'^edit/(?P<base_or_journey>\w+)',
        views.edit, name = 'events_admin_edit'),
    url(r'^deactivate/$', views.deactivate,
        name = 'events_admin_deactivate'),
    url(r'^import/$', views.import_data, name = 'import'),
]

