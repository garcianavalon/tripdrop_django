from django.conf.urls import url

import maps.views as maps_views

urlpatterns = [
    url(r'^base/', maps_views.BaseMapView.as_view(), name='base_map'),
]