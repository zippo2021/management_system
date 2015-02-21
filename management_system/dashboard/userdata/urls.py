from django.conf.urls import url
from dashboard.userdata import views

urlpatterns = [
	url(r'^add_document', views.document_wizard,
               name = 'userdata_document_wizard'),
    url(r'^edit', views.edit, name = 'userdata_edit'),
]
