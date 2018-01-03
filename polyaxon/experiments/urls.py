# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from experiments import views
from libs.urls import (
    UUID_PATTERN,
    USERNAME_PATTERN,
    NAME_PATTERN,
    SEQUENCE_PATTERN,
    EXPERIMENT_SEQUENCE_PATTERN)

experiments_urlpatterns = [
    # Get all experiments
    url(r'^experiments/?$', views.ExperimentListView.as_view()),
    url(r'^{}/{}/experiments/{}/?$'.format(USERNAME_PATTERN, NAME_PATTERN, SEQUENCE_PATTERN),
        views.ExperimentDetailView.as_view()),
    url(r'^{}/{}/experiments/{}/stop/?$'.format(USERNAME_PATTERN, NAME_PATTERN, SEQUENCE_PATTERN),
        views.ExperimentStopView.as_view()),
    url(r'^{}/{}/experiments/{}/restart/?$'.format(
        USERNAME_PATTERN, NAME_PATTERN, SEQUENCE_PATTERN),
        views.ExperimentRestartView.as_view()),
    url(r'^{}/{}/experiments/{}/statuses/?$'.format(
        USERNAME_PATTERN, NAME_PATTERN, EXPERIMENT_SEQUENCE_PATTERN),
        views.ExperimentStatusListView.as_view()),
    url(r'^{}/{}/experiments/{}/statuses/{}/?$'.format(
        USERNAME_PATTERN, NAME_PATTERN, EXPERIMENT_SEQUENCE_PATTERN, UUID_PATTERN),
        views.ExperimentStatusDetailView.as_view()),
    url(r'^{}/{}/experiments/{}/jobs/?$'.format(
        USERNAME_PATTERN, NAME_PATTERN, EXPERIMENT_SEQUENCE_PATTERN),
        views.ExperimentJobListView.as_view()),
]

jobs_urlpatterns = [
    url(r'^{}/{}/experiments/{}/jobs/{}/?$'.format(
        USERNAME_PATTERN, NAME_PATTERN, EXPERIMENT_SEQUENCE_PATTERN, SEQUENCE_PATTERN),
        views.ExperimentJobDetailView.as_view()),
    url(r'^{}/{}/experiments/{}/jobs/{}/statuses/?$'.format(
        USERNAME_PATTERN, NAME_PATTERN, EXPERIMENT_SEQUENCE_PATTERN, SEQUENCE_PATTERN),
        views.ExperimentJobStatusListView.as_view()),
    url(r'^{}/{}/experiments/{}/jobs/{}/statuses/{}/?$'.format(
        USERNAME_PATTERN, NAME_PATTERN, EXPERIMENT_SEQUENCE_PATTERN, SEQUENCE_PATTERN,
        UUID_PATTERN),
        views.ExperimentJobStatusDetailView.as_view()),
]

urlpatterns = format_suffix_patterns(experiments_urlpatterns + jobs_urlpatterns)
