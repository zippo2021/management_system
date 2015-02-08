from django.conf.urls import url
from dashboard.regular import views, forms

urlpatterns = [
	url(r'^edit', views.regular_user_wizard, name = 'edit_regular'),
	url(r'^completed', views.completed, name = 'regular_edited'),
	url(r'^self_profile_view',views.self_profile_view, name = 'self_profile_view'),
    url(r'^regular_profile_view/(?P<uid>\d+)/$',views.regular_profile_view, name = 'regular_profile_view'),
    url(r'toggle_regular_modal',views.toggle_regular_modal, name = 'toggle_regular_modal')
]
