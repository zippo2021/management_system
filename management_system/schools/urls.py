from django.conf.urls import url
from schools import views

urlpatterns = [
    url(r'^add', views.add, name = 'schools_add'),
    url(r'^edit/(?P<school_id>\d+)', views.edit, name = 'schools_edit'),
    url(r'^approve/(?P<school_id>\d+)',
        views.approve,
        name = 'schools_approve'),
    url(r'^show_unproved', views.show_unproved, name = 'schools_show_unproved'),
]
