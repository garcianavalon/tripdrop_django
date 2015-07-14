from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [  
	url(r'^needs/', include('needs.urls', namespace="needs")),
    url(r'^admin/', include(admin.site.urls)),
    (r'^accounts/', include('allauth.urls')),
]