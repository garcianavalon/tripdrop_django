from django.conf.urls import url

import needs.views as need_views

urlpatterns = [
    url(r'^$', need_views.NeedList.as_view(), name='list'),
    url(r'^add/$', need_views.NeedCreate.as_view(), name='add'),
    url(r'^(?P<need_id>[0-9]+)/$', need_views.NeedUpdate.as_view(), name='update'),
    url(r'^(?P<need_id>[0-9]+)/delete/$', need_views.NeedDelete.as_view(), name='delete'),
]