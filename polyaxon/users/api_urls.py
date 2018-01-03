# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from django.conf.urls import url
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.urlpatterns import format_suffix_patterns

from users import views

urlpatterns = [
    url(r'^users/?$',
        views.UserView.as_view()),
    url(r'^users/token/?$',
        obtain_auth_token),
]

urlpatterns = format_suffix_patterns(urlpatterns)
