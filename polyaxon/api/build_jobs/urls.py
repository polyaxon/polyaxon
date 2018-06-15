from rest_framework.urlpatterns import format_suffix_patterns

from django.urls import re_path

from api.build_jobs import views
from constants.urls import ID_PATTERN, JOB_ID_PATTERN, NAME_PATTERN, USERNAME_PATTERN, UUID_PATTERN

build_jobs_urlpatterns = [
    re_path(r'^{}/{}/builds/{}/?$'.format(USERNAME_PATTERN, NAME_PATTERN, ID_PATTERN),
            views.BuildDetailView.as_view()),
    re_path(r'^{}/{}/builds/{}/statuses/?$'.format(
        USERNAME_PATTERN, NAME_PATTERN, JOB_ID_PATTERN),
        views.BuildStatusListView.as_view()),
    re_path(r'^{}/{}/builds/{}/statuses/{}/?$'.format(
        USERNAME_PATTERN, NAME_PATTERN, JOB_ID_PATTERN, UUID_PATTERN),
        views.BuildStatusDetailView.as_view()),
    re_path(r'^{}/{}/builds/{}/logs/?$'.format(
        USERNAME_PATTERN, NAME_PATTERN, JOB_ID_PATTERN),
        views.BuildLogsView.as_view()),
    re_path(
        r'^{}/{}/builds/{}/stop/?$'.format(USERNAME_PATTERN, NAME_PATTERN, ID_PATTERN),
        views.BuildStopView.as_view()),
]

urlpatterns = format_suffix_patterns(build_jobs_urlpatterns)
