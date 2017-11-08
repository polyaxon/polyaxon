# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from experiments import views
from libs.urls import UUID_PATTERN, EXPERIMENT_UUID_PATTERN

urlpatterns = [
    url(r'^experiments/?$', views.ExperimentListView.as_view()),
    url(r'^experiments/{}/?$'.format(UUID_PATTERN), views.ExperimentDetailView.as_view()),
    url(r'^experiments/{}/jobs/?$'.format(EXPERIMENT_UUID_PATTERN),
        views.ExperimentJobListView.as_view()),
    url(r'^experiments/{}/jobs/{}/?$'.format(EXPERIMENT_UUID_PATTERN, UUID_PATTERN),
        views.ExperimentJobDetailView.as_view()),
    url(r'^experiments/{}/status/?$'.format(EXPERIMENT_UUID_PATTERN),
        views.ExperimentStatusListView.as_view()),
    url(r'^experiments/{}/status/{}/?$'.format(EXPERIMENT_UUID_PATTERN, UUID_PATTERN),
        views.ExperimentStatusDetailView.as_view()),
    # url(r'^experiments/{}/start/?$'.format(UUID_PATTERN), views.ExperimentStartView.as_view()),
    # url(r'^experiments/{}/status/?$'.format(UUID_PATTERN), views.ExperimentStartView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
