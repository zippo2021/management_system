from django.conf.urls import patterns, include, url

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
    url(r'^userdata/', include('dashboard.userdata.urls')),
    url(r'^teacher/', include('dashboard.teacher.urls')),
    url(r'^profile/', include('dashboard.common_profile.urls')),
    url(r'^regular/', include('dashboard.regular.urls')),
	url(r'^user_manager/', include('user_manager.urls')),
    url(r'^news/', include('news.urls')),
)
