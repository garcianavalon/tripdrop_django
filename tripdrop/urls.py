from django.conf.urls import include, url
from django.contrib import admin
from . import views

urlpatterns = [
	url(r'^$', views.IndexView.as_view(), name='index'),
	url(r'^needs/', include('needs.urls', namespace="needs")),
	url(r'^maps/', include('maps.urls', namespace="maps")),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^', include('users.urls', namespace="users")),
]