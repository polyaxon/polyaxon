from rest_framework.urlpatterns import format_suffix_patterns

from django.urls import re_path

from api.archives import views
from constants.urls import USERNAME_PATTERN

build_jobs_urlpatterns = [
    re_path(r'^archives/{}/projects/?$'.format(USERNAME_PATTERN),
            views.ProjectArchiveListView.as_view()),
    re_path(r'^archives/{}/groups/?$'.format(USERNAME_PATTERN),
            views.ExperimentGroupArchiveListView.as_view()),
    re_path(r'^archives/{}/experiments/?$'.format(USERNAME_PATTERN),
            views.ExperimentArchiveListView.as_view()),
    re_path(r'^archives/{}/builds/?$'.format(USERNAME_PATTERN),
            views.BuildArchiveListView.as_view()),
    re_path(r'^archives/{}/jobs/?$'.format(USERNAME_PATTERN),
            views.JobArchiveListView.as_view()),
]

urlpatterns = format_suffix_patterns(build_jobs_urlpatterns)
