from django.conf.urls import url

import needs.views as need_views

urlpatterns = [

    url(r'^municipalities/$', need_views.list_municipalities, name='list_municipalities'),

    url(r'^$', need_views.NeedList.as_view(), name='list'),
    url(r'^create/$', need_views.NeedCreate.as_view(), name='create'),
    url(r'^(?P<slug>[-\w]+)/$', need_views.NeedDetail.as_view(), name='detail'),
    url(r'^(?P<slug>[-\w]+)/update/$', need_views.NeedUpdate.as_view(), name='update'),
    url(r'^(?P<slug>[-\w]+)/delete/$', need_views.NeedDelete.as_view(), name='delete'),
]