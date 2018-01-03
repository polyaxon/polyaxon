# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from django.conf.urls import url
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.urlpatterns import format_suffix_patterns

from libs.urls import USERNAME_PATTERN
from users import views

urlpatterns = [
    url(r'^users/?$',
        views.UserView.as_view()),
    url(r'^users/token/?$',
        obtain_auth_token),
    url(r'^users/activate/{}/?$'.format(USERNAME_PATTERN),
        views.ActivateView.as_view()),
    url(r'^users/delete/{}/?$'.format(USERNAME_PATTERN),
        views.DeleteView.as_view()),
    url(r'^superusers/grant/{}/?$'.format(USERNAME_PATTERN),
        views.GrantSuperuserView.as_view()),
    url(r'^superusers/revoke/{}/?$'.format(USERNAME_PATTERN),
        views.RevokeSuperuserView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
