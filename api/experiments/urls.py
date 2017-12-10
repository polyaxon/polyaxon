# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns

from experiments import views
from libs.urls import (
    UUID_PATTERN,
    EXPERIMENT_UUID_PATTERN,
    JOB_UUID_PATTERN,
)

experiments_urlpatterns = [
    # Get all experiments
    url(r'^experiments/?$', views.ExperimentListView.as_view()),
    url(r'^experiments/{}/?$'.format(UUID_PATTERN), views.ExperimentDetailView.as_view()),
    url(r'^experiments/{}/status/?$'.format(EXPERIMENT_UUID_PATTERN),
        views.ExperimentStatusListView.as_view()),
    url(r'^experiments/{}/status/{}/?$'.format(EXPERIMENT_UUID_PATTERN, UUID_PATTERN),
        views.ExperimentStatusDetailView.as_view()),
    url(r'^experiments/{}/jobs/?$'.format(EXPERIMENT_UUID_PATTERN),
        views.ExperimentJobListView.as_view()),
    # url(r'^experiments/{}/stop/?$'.format(UUID_PATTERN), views.ExperimentStopView.as_view()),
    url(r'^experiments/{}/restart/?$'.format(UUID_PATTERN), views.ExperimentRestartView.as_view()),
]

jobs_urlpatterns = [
    url(r'^jobs/{}/?$'.format(UUID_PATTERN), views.ExperimentJobDetailView.as_view()),
    url(r'^jobs/{}/status/?$'.format(JOB_UUID_PATTERN), views.ExperimentJobStatusListView.as_view()),
    url(r'^jobs/{}/status/{}/?$'.format(JOB_UUID_PATTERN, UUID_PATTERN),
        views.ExperimentJobStatusDetailView.as_view()),
]

nested_experiments_urlpatterns = [
    # Get all experiment under a project
    url(r'^projects/{}/experiments/?$'.format(UUID_PATTERN),
        views.ProjectExperimentListView.as_view()),

    # Get all experiments under a group
    url(r'^experiment_groups/{}/experiments/?$'.format(UUID_PATTERN),
        views.GroupExperimentListView.as_view()),
]

urlpatterns = format_suffix_patterns(
    experiments_urlpatterns +
    jobs_urlpatterns +
    nested_experiments_urlpatterns)
