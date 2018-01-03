# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from libs.urls import USERNAME_PATTERN, NAME_PATTERN
from repos import views

urlpatterns = [
    url(r'^{}/{}/repo/?$'.format(USERNAME_PATTERN, NAME_PATTERN),
        views.RepoDetailView.as_view()),
    url(r'^{}/{}/repo/upload/?$'.format(USERNAME_PATTERN, NAME_PATTERN),
        views.UploadFilesView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
