from django.conf.urls import url
from dashboard.userdata import views

urlpatterns = [
	url(r'^add_document', views.document_wizard, name = 'add_userdata_document'),
    url(r'^tmp_base', views.tmp_base, name = 'tmp_base'),
    url(r'^edit', views.edit, name = 'userdata_edit'),
    url(r'^completed', views.completed, name = 'userdata_edited'),
    url(r'^base_profile_view', views.base_profile_view, name = 'base_profile_view'),
]
