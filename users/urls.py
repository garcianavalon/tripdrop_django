from django.conf.urls import url

import users.views as user_views

urlpatterns = [
    url(r'^accounts/profile/', user_views.ProfileView.as_view(), name='profile'),
]