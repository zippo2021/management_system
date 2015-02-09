from django.conf.urls import url
from schools import views

urlpatterns = [
    #test url: index
    url(r'^index', views.index, name = 'schools_index'),
    url(r'^add', views.add, name = 'schools_add'),
    url(r'^edit/(?P<school_id>\d+)', views.edit, name = 'schools_edit'),
    url(r'^approve/(?P<school_id>\d+)',
        views.approve,
        name = 'schools_approve'),

    url(r'^approve_completed',
        views.approve_completed,
        name = 'schools_approve_completed'),

    url(r'^add_completed',
        views.add_completed,
        name = 'schools_add_completed'),
    url(r'^show_unproved', views.show_unproved, name = 'schools_show_unproved'),
]
