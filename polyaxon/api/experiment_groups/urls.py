from rest_framework.urlpatterns import format_suffix_patterns

from django.urls import re_path

from api.experiment_groups import views
from api.experiments import views as experiments_views
from constants.urls import NAME_PATTERN, SEQUENCE_PATTERN, USERNAME_PATTERN

groups_urlpatterns = [
    re_path(r'^{}/{}/groups/{}/?$'.format(USERNAME_PATTERN, NAME_PATTERN, SEQUENCE_PATTERN),
            views.ExperimentGroupDetailView.as_view()),
    re_path(
        r'^{}/{}/groups/{}/experiments/?$'.format(USERNAME_PATTERN, NAME_PATTERN, SEQUENCE_PATTERN),
        experiments_views.GroupExperimentListView.as_view()),
    re_path(r'^{}/{}/groups/{}/stop/?$'.format(USERNAME_PATTERN, NAME_PATTERN, SEQUENCE_PATTERN),
            views.ExperimentGroupStopView.as_view()),
]

# Order is important, because the patterns could swallow other urls
urlpatterns = format_suffix_patterns(groups_urlpatterns)
