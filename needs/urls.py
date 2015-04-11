from django.conf.urls import url

import needs.views as need_views

urlpatterns = [
    url(r'^$', need_views.NeedList.as_view(), name='list'),
]