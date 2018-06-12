from rest_framework.urlpatterns import format_suffix_patterns

from django.urls import re_path

from api.jobs import views
from constants.urls import (
    JOB_SEQUENCE_PATTERN,
    NAME_PATTERN,
    SEQUENCE_PATTERN,
    USERNAME_PATTERN,
    UUID_PATTERN
)

jobs_urlpatterns = [
    re_path(r'^{}/{}/jobs/{}/?$'.format(USERNAME_PATTERN, NAME_PATTERN, SEQUENCE_PATTERN),
            views.JobDetailView.as_view()),
    re_path(r'^{}/{}/job/{}/restart/?$'.format(
        USERNAME_PATTERN, NAME_PATTERN, SEQUENCE_PATTERN),
        views.JobRestartView.as_view()),
    re_path(r'^{}/{}/jobs/{}/statuses/?$'.format(
        USERNAME_PATTERN, NAME_PATTERN, JOB_SEQUENCE_PATTERN),
        views.JobStatusListView.as_view()),
    re_path(r'^{}/{}/jobs/{}/statuses/{}/?$'.format(
        USERNAME_PATTERN, NAME_PATTERN, JOB_SEQUENCE_PATTERN, UUID_PATTERN),
        views.JobStatusDetailView.as_view()),
    re_path(r'^{}/{}/jobs/{}/logs/?$'.format(
        USERNAME_PATTERN, NAME_PATTERN, JOB_SEQUENCE_PATTERN),
        views.JobLogsView.as_view()),
    re_path(
        r'^{}/{}/jobs/{}/stop/?$'.format(USERNAME_PATTERN, NAME_PATTERN, SEQUENCE_PATTERN),
        views.JobStopView.as_view()),
]

urlpatterns = format_suffix_patterns(jobs_urlpatterns)
