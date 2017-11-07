# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from libs.urls import UUID_PATTERN, PROJECT_UUID_PATTERN
from projects import views

urlpatterns = [
    url(r'^projects/?$',
        views.ProjectListView.as_view()),
    url(r'^projects/{}/?$'.format(UUID_PATTERN),
        views.ProjectDetailView.as_view()),
    url(r'^projects/{}/polyaxonfiles?$'.format(PROJECT_UUID_PATTERN),
        views.ProjectPolyaxonfileListView.as_view()),
    url(r'^projects/{}/polyaxonfiles/{}?$'.format(PROJECT_UUID_PATTERN, UUID_PATTERN),
        views.ProjectPolyaxonfileDetailView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
