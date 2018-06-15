from rest_framework.urlpatterns import format_suffix_patterns

from django.urls import re_path

from api.jobs import views
from constants.urls import ID_PATTERN, JOB_ID_PATTERN, NAME_PATTERN, USERNAME_PATTERN, UUID_PATTERN

jobs_urlpatterns = [
    re_path(r'^{}/{}/jobs/{}/?$'.format(USERNAME_PATTERN, NAME_PATTERN, ID_PATTERN),
            views.JobDetailView.as_view()),
    re_path(r'^{}/{}/jobs/{}/restart/?$'.format(
        USERNAME_PATTERN, NAME_PATTERN, ID_PATTERN),
        views.JobRestartView.as_view()),
    re_path(r'^{}/{}/jobs/{}/statuses/?$'.format(
        USERNAME_PATTERN, NAME_PATTERN, JOB_ID_PATTERN),
        views.JobStatusListView.as_view()),
    re_path(r'^{}/{}/jobs/{}/statuses/{}/?$'.format(
        USERNAME_PATTERN, NAME_PATTERN, JOB_ID_PATTERN, UUID_PATTERN),
        views.JobStatusDetailView.as_view()),
    re_path(r'^{}/{}/jobs/{}/logs/?$'.format(
        USERNAME_PATTERN, NAME_PATTERN, JOB_ID_PATTERN),
        views.JobLogsView.as_view()),
    re_path(
        r'^{}/{}/jobs/{}/stop/?$'.format(USERNAME_PATTERN, NAME_PATTERN, ID_PATTERN),
        views.JobStopView.as_view()),
]

urlpatterns = format_suffix_patterns(jobs_urlpatterns)
