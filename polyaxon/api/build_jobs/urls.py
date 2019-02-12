from rest_framework.urlpatterns import format_suffix_patterns

from django.urls import re_path

from api.bookmarks import views as bookmark_views
from api.build_jobs import views
from constants.urls import BUILD_ID_PATTERN, OWNER_NAME_PATTERN, PROJECT_NAME_PATTERN, UUID_PATTERN

build_jobs_urlpatterns = [
    re_path(
        r'^{}/{}/builds/{}/?$'.format(OWNER_NAME_PATTERN, PROJECT_NAME_PATTERN, BUILD_ID_PATTERN),
        views.BuildDetailView.as_view()),
    re_path(r'^{}/{}/builds/{}/archive/?$'.format(
        OWNER_NAME_PATTERN, PROJECT_NAME_PATTERN, BUILD_ID_PATTERN),
        views.BuildArchiveView.as_view()),
    re_path(r'^{}/{}/builds/{}/restore/?$'.format(
        OWNER_NAME_PATTERN, PROJECT_NAME_PATTERN, BUILD_ID_PATTERN),
        views.BuildRestoreView.as_view()),
    re_path(r'^{}/{}/builds/{}/statuses/?$'.format(
        OWNER_NAME_PATTERN, PROJECT_NAME_PATTERN, BUILD_ID_PATTERN),
        views.BuildStatusListView.as_view()),
    re_path(r'^{}/{}/builds/{}/statuses/{}/?$'.format(
        OWNER_NAME_PATTERN, PROJECT_NAME_PATTERN, BUILD_ID_PATTERN, UUID_PATTERN),
        views.BuildStatusDetailView.as_view()),
    re_path(r'^{}/{}/builds/{}/logs/?$'.format(
        OWNER_NAME_PATTERN, PROJECT_NAME_PATTERN, BUILD_ID_PATTERN),
        views.BuildLogsView.as_view()),
    re_path(r'^{}/{}/builds/{}/stop/?$'.format(
        OWNER_NAME_PATTERN, PROJECT_NAME_PATTERN, BUILD_ID_PATTERN),
        views.BuildStopView.as_view()),
    re_path(r'^{}/{}/builds/{}/_heartbeat/?$'.format(
        OWNER_NAME_PATTERN, PROJECT_NAME_PATTERN, BUILD_ID_PATTERN),
        views.BuildHeartBeatView.as_view()),
    re_path(r'^{}/{}/builds/{}/bookmark/?$'.format(
        OWNER_NAME_PATTERN, PROJECT_NAME_PATTERN, BUILD_ID_PATTERN),
        bookmark_views.BuildJobBookmarkCreateView.as_view()),
    re_path(r'^{}/{}/builds/{}/unbookmark/?$'.format(
        OWNER_NAME_PATTERN, PROJECT_NAME_PATTERN, BUILD_ID_PATTERN),
        bookmark_views.BuildJobBookmarkDeleteView.as_view()),
]

urlpatterns = format_suffix_patterns(build_jobs_urlpatterns)
