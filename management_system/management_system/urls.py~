from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'management_system.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^accounts/', include('registration.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'helpdesk/', include('helpdesk.urls')),
    url(r'define_user/', include('define_user.urls')),
    url(r'edit_userdata/', include('edit_userdata.urls')),
    
)
