from rest_framework.urlpatterns import format_suffix_patterns

from django.urls import re_path

from api.bookmarks import views as bookmark_views
from api.experiment_groups import views
from constants.urls import GROUP_ID_PATTERN, ID_PATTERN, NAME_PATTERN, USERNAME_PATTERN

groups_urlpatterns = [
    re_path(r'^{}/{}/groups/{}/?$'.format(USERNAME_PATTERN, NAME_PATTERN, ID_PATTERN),
            views.ExperimentGroupDetailView.as_view()),
    re_path(r'^{}/{}/groups/{}/statuses/?$'.format(
        USERNAME_PATTERN, NAME_PATTERN, GROUP_ID_PATTERN),
        views.ExperimentGroupStatusListView.as_view()),
    re_path(r'^{}/{}/groups/{}/stop/?$'.format(USERNAME_PATTERN, NAME_PATTERN, ID_PATTERN),
            views.ExperimentGroupStopView.as_view()),
    re_path(
        r'^{}/{}/groups/{}/bookmark/?$'.format(USERNAME_PATTERN, NAME_PATTERN, ID_PATTERN),
        bookmark_views.ExperimentGroupBookmarkCreateView.as_view()),
    re_path(
        r'^{}/{}/groups/{}/unbookmark/?$'.format(USERNAME_PATTERN, NAME_PATTERN, ID_PATTERN),
        bookmark_views.ExperimentGroupBookmarkDeleteView.as_view()),
    re_path(r'^{}/{}/groups/{}/chartviews/?$'.format(
        USERNAME_PATTERN, NAME_PATTERN, GROUP_ID_PATTERN),
        views.ExperimentGroupChartViewListView.as_view()),
    re_path(r'^{}/{}/groups/{}/chartviews/{}/?$'.format(
        USERNAME_PATTERN, NAME_PATTERN, GROUP_ID_PATTERN, ID_PATTERN),
        views.ExperimentGroupChartViewDetailView.as_view()),
]

# Order is important, because the patterns could swallow other urls
urlpatterns = format_suffix_patterns(groups_urlpatterns)
