# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from django.urls import re_path
from rest_framework.urlpatterns import format_suffix_patterns

from libs.urls import USERNAME_PATTERN, NAME_PATTERN, SEQUENCE_PATTERN
from experiments import views as experiments_views
from plugins import views as plugins_views
from projects import views

projects_urlpatterns = [
    re_path(r'^projects/?$',
            views.ProjectCreateView.as_view()),
    re_path(r'^{}/?$'.format(USERNAME_PATTERN),
            views.ProjectListView.as_view()),
    re_path(r'^{}/{}/?$'.format(USERNAME_PATTERN, NAME_PATTERN),
            views.ProjectDetailView.as_view()),
    re_path(r'^{}/{}/tensorboard/start/?$'.format(USERNAME_PATTERN, NAME_PATTERN),
            plugins_views.StartTensorboardView.as_view()),
    re_path(r'^{}/{}/tensorboard/stop/?$'.format(USERNAME_PATTERN, NAME_PATTERN),
            plugins_views.StopTensorboardView.as_view()),
    re_path(r'^{}/{}/notebook/start/?$'.format(USERNAME_PATTERN, NAME_PATTERN),
            plugins_views.StartNotebookView.as_view()),
    re_path(r'^{}/{}/notebook/stop/?$'.format(USERNAME_PATTERN, NAME_PATTERN),
            plugins_views.StopNotebookView.as_view()),
    re_path(r'^{}/{}/groups/?$'.format(USERNAME_PATTERN, NAME_PATTERN),
            views.ExperimentGroupListView.as_view()),
    # Get all experiment under a project
    re_path(r'^{}/{}/experiments/?$'.format(USERNAME_PATTERN, NAME_PATTERN),
            experiments_views.ProjectExperimentListView.as_view()),

    re_path(r'^{}/{}/groups/{}/?$'.format(USERNAME_PATTERN, NAME_PATTERN, SEQUENCE_PATTERN),
            views.ExperimentGroupDetailView.as_view()),
    re_path(r'^{}/{}/groups/{}/stop/?$'.format(USERNAME_PATTERN, NAME_PATTERN, SEQUENCE_PATTERN),
            views.ExperimentGroupStopView.as_view()),
    re_path(
        r'^{}/{}/groups/{}/experiments/?$'.format(USERNAME_PATTERN, NAME_PATTERN, SEQUENCE_PATTERN),
        experiments_views.GroupExperimentListView.as_view()),
]

# Order is important, because the patterns could swallow other urls
urlpatterns = format_suffix_patterns(projects_urlpatterns)
