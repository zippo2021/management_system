from django.conf.urls import patterns, url

from events.study_groups import views

urlpatterns = patterns('',
    url(r'^groups/$', views.index, name='index'),

    url(r'^groups/new_group$', views.add_group, name='add_group'),
    url(r'^groups/delete_group$', views.delete_group, name='delete_group'),
    url(r'^groups/get_group_info$', views.get_group_info, name='get_group_info'),
    url(r'^groups/save_group_members$', views.save_group_members, name='save_group_members'),
)