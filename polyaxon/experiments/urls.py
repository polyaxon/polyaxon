from rest_framework.urlpatterns import format_suffix_patterns

from django.urls import re_path

from experiments import views
from libs.urls import (
    EXPERIMENT_SEQUENCE_PATTERN,
    NAME_PATTERN,
    SEQUENCE_PATTERN,
    USERNAME_PATTERN,
    UUID_PATTERN
)

experiments_urlpatterns = [
    # Get all experiments
    re_path(r'^experiments/?$', views.ExperimentListView.as_view()),
    re_path(r'^{}/{}/experiments/{}/?$'.format(USERNAME_PATTERN, NAME_PATTERN, SEQUENCE_PATTERN),
            views.ExperimentDetailView.as_view()),
    re_path(r'^{}/{}/experiments/{}/restart/?$'.format(
        USERNAME_PATTERN, NAME_PATTERN, SEQUENCE_PATTERN),
        views.ExperimentRestartView.as_view()),
    re_path(r'^{}/{}/experiments/{}/resume/?$'.format(
        USERNAME_PATTERN, NAME_PATTERN, SEQUENCE_PATTERN),
        views.ExperimentResumeView.as_view()),
    re_path(r'^{}/{}/experiments/{}/statuses/?$'.format(
        USERNAME_PATTERN, NAME_PATTERN, EXPERIMENT_SEQUENCE_PATTERN),
        views.ExperimentStatusListView.as_view()),
    re_path(r'^{}/{}/experiments/{}/metrics/?$'.format(
        USERNAME_PATTERN, NAME_PATTERN, EXPERIMENT_SEQUENCE_PATTERN),
        views.ExperimentMetricListView.as_view()),
    re_path(r'^{}/{}/experiments/{}/statuses/{}/?$'.format(
        USERNAME_PATTERN, NAME_PATTERN, EXPERIMENT_SEQUENCE_PATTERN, UUID_PATTERN),
        views.ExperimentStatusDetailView.as_view()),
    re_path(r'^{}/{}/experiments/{}/jobs/?$'.format(
        USERNAME_PATTERN, NAME_PATTERN, EXPERIMENT_SEQUENCE_PATTERN),
        views.ExperimentJobListView.as_view()),
    re_path(r'^{}/{}/experiments/{}/logs/?$'.format(
        USERNAME_PATTERN, NAME_PATTERN, EXPERIMENT_SEQUENCE_PATTERN),
        views.ExperimentLogsView.as_view()),
]

jobs_urlpatterns = [
    re_path(r'^{}/{}/experiments/{}/jobs/{}/?$'.format(
        USERNAME_PATTERN, NAME_PATTERN, EXPERIMENT_SEQUENCE_PATTERN, SEQUENCE_PATTERN),
        views.ExperimentJobDetailView.as_view()),
    re_path(r'^{}/{}/experiments/{}/jobs/{}/statuses/?$'.format(
        USERNAME_PATTERN, NAME_PATTERN, EXPERIMENT_SEQUENCE_PATTERN, SEQUENCE_PATTERN),
        views.ExperimentJobStatusListView.as_view()),
    re_path(r'^{}/{}/experiments/{}/jobs/{}/statuses/{}/?$'.format(
        USERNAME_PATTERN, NAME_PATTERN, EXPERIMENT_SEQUENCE_PATTERN, SEQUENCE_PATTERN,
        UUID_PATTERN),
        views.ExperimentJobStatusDetailView.as_view()),
]

urlpatterns = format_suffix_patterns(experiments_urlpatterns + jobs_urlpatterns)
