from django.conf.urls import url
from dashboard.regular import views, forms

urlpatterns = [
	url(r'^edit/regular', views.regular_user_wizard,
                        name = 'regular_user_wizard'),
    
#	url(r'^transfer', views.transfer,
#                        name = 'transfer'),
]
