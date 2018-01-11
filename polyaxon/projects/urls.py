# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from libs.urls import USERNAME_PATTERN, NAME_PATTERN, SEQUENCE_PATTERN
from experiments import views as experiments_views
from projects import views

projects_urlpatterns = [
    url(r'^projects/?$',
        views.ProjectCreateView.as_view()),
    url(r'^{}/?$'.format(USERNAME_PATTERN),
        views.ProjectListView.as_view()),
    url(r'^{}/{}/?$'.format(USERNAME_PATTERN, NAME_PATTERN),
        views.ProjectDetailView.as_view()),
    url(r'^{}/{}/tensorboard/start/?$'.format(USERNAME_PATTERN, NAME_PATTERN),
        views.StartTensorboardView.as_view()),
    url(r'^{}/{}/tensorboard/stop/?$'.format(USERNAME_PATTERN, NAME_PATTERN),
        views.StopTensorboardView.as_view()),
    url(r'^{}/{}/groups/?$'.format(USERNAME_PATTERN, NAME_PATTERN),
        views.ExperimentGroupListView.as_view()),
    # Get all experiment under a project
    url(r'^{}/{}/experiments/?$'.format(USERNAME_PATTERN, NAME_PATTERN),
        experiments_views.ProjectExperimentListView.as_view()),

    url(r'^{}/{}/groups/{}/?$'.format(USERNAME_PATTERN, NAME_PATTERN, SEQUENCE_PATTERN),
        views.ExperimentGroupDetailView.as_view()),
    url(r'^{}/{}/groups/{}/experiments/?$'.format(USERNAME_PATTERN, NAME_PATTERN, SEQUENCE_PATTERN),
        experiments_views.GroupExperimentListView.as_view()),
]

# Order is important, because the patterns could swallow other urls
urlpatterns = format_suffix_patterns(projects_urlpatterns)
