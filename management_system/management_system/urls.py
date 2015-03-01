from django.conf.urls import patterns, include, url

from management_system import views
from events import events_admin
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'management_system.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^schools/', include('schools.urls')),
    url(r'^accounts/', include('registration.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^helpdesk/', include('helpdesk.urls')),
    url(r'^common_profile/', include('dashboard.userdata.urls')),
    url(r'^common_profile/', include('dashboard.teacher.urls')),
    url(r'^common_profile/', include('dashboard.common_profile.urls')),
    url(r'^common_profile/', include('dashboard.regular.urls')),
	url(r'^user_manager/', include('user_manager.urls')),
    url(r'^news/', include('news.urls')),
    url(r'^event/(?P<event_id>\d+)/', include('events.events_manage.urls')),
    url(r'^event/(?P<event_id>\d+)/', include('events.events_admin.urls')),
    url(r'^event/(?P<event_id>\d+)/', include('events.price_groups.urls')),
    url(r'^event/add', events_admin.views.event_wizard,
                        name = 'events_admin_event_wizard'),
    url(r'^completed', views.completed, name = 'completed'),
    url(r'^feedback/', include('feedback.urls')),
    url(r'^event/(?P<event_id>\d+)/', include('events.study_groups.urls')),
    url(r'^event/(?P<event_id>\d+)/', include('events.journal.urls')),
    (r'^upload/$','uppload'),
    url(r'^',views.index,name='index'),
)
