from rest_framework.urlpatterns import format_suffix_patterns

from django.urls import re_path

from api.bookmarks import views
from constants.urls import USERNAME_PATTERN

build_jobs_urlpatterns = [
    re_path(r'^bookmarks/{}/projects/?$'.format(USERNAME_PATTERN),
            views.ProjectBookmarkListView.as_view()),
    re_path(r'^bookmarks/{}/groups/?$'.format(USERNAME_PATTERN),
            views.ExperimentGroupBookmarkListView.as_view()),
    re_path(r'^bookmarks/{}/experiments/?$'.format(USERNAME_PATTERN),
            views.ExperimentBookmarkListView.as_view()),
    re_path(r'^bookmarks/{}/builds/?$'.format(USERNAME_PATTERN),
            views.BuildBookmarkListView.as_view()),
    re_path(r'^bookmarks/{}/jobs/?$'.format(USERNAME_PATTERN),
            views.JobBookmarkListView.as_view()),
]

urlpatterns = format_suffix_patterns(build_jobs_urlpatterns)
