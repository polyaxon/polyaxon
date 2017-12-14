# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from libs.urls import UUID_PATTERN, USERNAME_PATTERN, NAME_PATTERN
from experiments import views as experiments_views
from projects import views

projects_urlpatterns = [
    url(r'^projects/?$',
        views.ProjectCreateView.as_view()),
    url(r'^{}/?$'.format(USERNAME_PATTERN),
        views.ProjectListView.as_view()),
    url(r'^{}/{}/?$'.format(USERNAME_PATTERN, NAME_PATTERN),
        views.ProjectDetailView.as_view()),
    url(r'^{}/{}/experiment_groups/?$'.format(USERNAME_PATTERN, NAME_PATTERN),
        views.ExperimentGroupListView.as_view()),
    # Get all experiment under a project
    url(r'^{}/{}/experiments/?$'.format(USERNAME_PATTERN, NAME_PATTERN),
        experiments_views.ProjectExperimentListView.as_view()),
]

experiment_groups_urlpatterns = [
    url(r'^experiment_groups/{}/?$'.format(UUID_PATTERN),
        views.ExperimentGroupDetailView.as_view()),

    # Get all experiments under a group
    url(r'^experiment_groups/{}/experiments/?$'.format(UUID_PATTERN),
        experiments_views.GroupExperimentListView.as_view()),
]

# Order is important, because the patterns could swallow other urls
urlpatterns = format_suffix_patterns(experiment_groups_urlpatterns + projects_urlpatterns)
