from django.conf.urls import patterns, url

from events.study_groups import views

urlpatterns = patterns('',
    url(r'^study_groups/$', views.index, name='study_groups_index'),

    url(r'^study_groups/new_group$', views.add_group, name='study_groups_add_group'),
    url(r'^study_groups/delete_group$', views.delete_group, name='study_groups_delete_group'),
    url(r'^study_groups/get_group_info$', views.get_group_info, name='study_groups_get_group_info'),
    url(r'^study_groups/save_group_members$', views.save_group_members, name='study_groups_save_group_members'),
)