from rest_framework.urlpatterns import format_suffix_patterns

from django.urls import re_path

from api.bookmarks import views as bookmark_views
from api.experiment_groups import views
from constants.urls import (
    GROUP_ID_PATTERN,
    ID_PATTERN,
    NAME_PATTERN,
    OWNER_NAME_PATTERN,
    PROJECT_NAME_PATTERN,
    USERNAME_PATTERN
)

groups_urlpatterns = [
    re_path(r'^{}/{}/groups/{}/?$'.format(
        OWNER_NAME_PATTERN, PROJECT_NAME_PATTERN, GROUP_ID_PATTERN),
        views.ExperimentGroupDetailView.as_view()),
    re_path(r'^{}/{}/selections/{}/?$'.format(
        OWNER_NAME_PATTERN, PROJECT_NAME_PATTERN, GROUP_ID_PATTERN),
        views.ExperimentGroupSelectionView.as_view()),
    re_path(r'^{}/{}/groups/{}/archive/?$'.format(
        OWNER_NAME_PATTERN, PROJECT_NAME_PATTERN, GROUP_ID_PATTERN),
        views.ExperimentGroupArchiveView.as_view()),
    re_path(r'^{}/{}/groups/{}/restore/?$'.format(
        OWNER_NAME_PATTERN, PROJECT_NAME_PATTERN, GROUP_ID_PATTERN),
        views.ExperimentGroupRestoreView.as_view()),
    re_path(r'^{}/{}/groups/{}/statuses/?$'.format(
        OWNER_NAME_PATTERN, PROJECT_NAME_PATTERN, GROUP_ID_PATTERN),
        views.ExperimentGroupStatusListView.as_view()),
    re_path(r'^{}/{}/groups/{}/metrics/?$'.format(
        OWNER_NAME_PATTERN, PROJECT_NAME_PATTERN, GROUP_ID_PATTERN),
        views.ExperimentGroupMetricsListView.as_view()),
    re_path(r'^{}/{}/groups/{}/stop/?$'.format(USERNAME_PATTERN, NAME_PATTERN, ID_PATTERN),
            views.ExperimentGroupStopView.as_view()),
    re_path(r'^{}/{}/groups/{}/bookmark/?$'.format(
        OWNER_NAME_PATTERN, PROJECT_NAME_PATTERN, GROUP_ID_PATTERN),
        bookmark_views.ExperimentGroupBookmarkCreateView.as_view()),
    re_path(r'^{}/{}/groups/{}/unbookmark/?$'.format(
        OWNER_NAME_PATTERN, PROJECT_NAME_PATTERN, GROUP_ID_PATTERN),
        bookmark_views.ExperimentGroupBookmarkDeleteView.as_view()),
    re_path(r'^{}/{}/groups/{}/chartviews/?$'.format(
        OWNER_NAME_PATTERN, PROJECT_NAME_PATTERN, GROUP_ID_PATTERN),
        views.ExperimentGroupChartViewListView.as_view()),
    re_path(r'^{}/{}/groups/{}/chartviews/{}/?$'.format(
        OWNER_NAME_PATTERN, PROJECT_NAME_PATTERN, GROUP_ID_PATTERN, ID_PATTERN),
        views.ExperimentGroupChartViewDetailView.as_view()),
]

# Order is important, because the patterns could swallow other urls
urlpatterns = format_suffix_patterns(groups_urlpatterns)
