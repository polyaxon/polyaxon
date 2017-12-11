# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from libs.urls import UUID_PATTERN
from projects import views

projects_urlpatterns = [
    url(r'^projects/?$',
        views.ProjectListView.as_view()),
    url(r'^projects/{}/?$'.format(UUID_PATTERN),
        views.ProjectDetailView.as_view()),
    url(r'^projects/{}/experiment_groups/?$'.format(UUID_PATTERN),
        views.ExperimentGroupListView.as_view()),
]

experiment_groups_urlpatterns = [
    url(r'^experiment_groups/{}/?$'.format(UUID_PATTERN),
        views.ExperimentGroupDetailView.as_view()),
]

urlpatterns = format_suffix_patterns(projects_urlpatterns + experiment_groups_urlpatterns)
