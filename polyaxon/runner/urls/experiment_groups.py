from rest_framework.urlpatterns import format_suffix_patterns

from django.urls import re_path

from libs.urls import NAME_PATTERN, SEQUENCE_PATTERN, USERNAME_PATTERN
import runner.apis.experiment_groups as views

groups_urlpatterns = [
    re_path(r'^{}/{}/groups/{}/stop/?$'.format(USERNAME_PATTERN, NAME_PATTERN, SEQUENCE_PATTERN),
            views.ExperimentGroupStopView.as_view()),
]

# Order is important, because the patterns could swallow other urls
urlpatterns = format_suffix_patterns(groups_urlpatterns)
