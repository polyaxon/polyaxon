# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns

from experiments import views
from libs.urls import (
    UUID_PATTERN,
    EXPERIMENT_UUID_PATTERN,
    EXPERIMENT_JOB_UUID_PATTERN,
    PROJECT_UUID_PATTERN,
    POLYAXON_SPEC_UUID_PATTERN,
)

patterns = [
    url(r'^experiments/?$', views.ExperimentListView.as_view()),
    url(r'^experiments/{}/?$'.format(UUID_PATTERN), views.ExperimentDetailView.as_view()),
    url(r'^experiments/{}/status/?$'.format(EXPERIMENT_UUID_PATTERN),
        views.ExperimentStatusListView.as_view()),
    url(r'^experiments/{}/status/{}/?$'.format(EXPERIMENT_UUID_PATTERN, UUID_PATTERN),
        views.ExperimentStatusDetailView.as_view()),
    url(r'^experiments/{}/jobs/?$'.format(EXPERIMENT_UUID_PATTERN),
        views.ExperimentJobListView.as_view()),
    url(r'^experiments/{}/jobs/{}/?$'.format(EXPERIMENT_UUID_PATTERN, UUID_PATTERN),
        views.ExperimentJobDetailView.as_view()),
    url(r'^experiments/{}/jobs/{}/status/?$'.format(EXPERIMENT_UUID_PATTERN,
                                                    EXPERIMENT_JOB_UUID_PATTERN),
        views.ExperimentJobStatusListView.as_view()),
    url(r'^experiments/{}/jobs/{}/status/{}/?$'.format(EXPERIMENT_UUID_PATTERN,
                                                       EXPERIMENT_JOB_UUID_PATTERN,
                                                       UUID_PATTERN),
        views.ExperimentJobStatusDetailView.as_view()),
    url(r'^experiments/{}/restart/?$'.format(UUID_PATTERN), views.ExperimentRestartView.as_view()),
]

urlpatterns = (patterns +
               [url(r'^projects/{}/'.format(PROJECT_UUID_PATTERN),
                    include(patterns))] +
               [url(r'^specs/{}/'.format(POLYAXON_SPEC_UUID_PATTERN),
                    include(patterns))]
               )

urlpatterns = format_suffix_patterns(urlpatterns)
