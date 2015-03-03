from django.conf.urls import url
from search import views

urlpatterns = [
    url(r'^user_search/$', views.user_search, name='user_search'),
]

