from django.conf.urls import url
from news import views

urlpatterns = [
	url(r'^main/', views.main, name = 'news_main'),
]
