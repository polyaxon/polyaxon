from rest_framework.urlpatterns import format_suffix_patterns

from django.urls import re_path

from libs.urls import (
    NAME_PATTERN,
    SEQUENCE_PATTERN,
    USERNAME_PATTERN,
)
import runner.apis.experiments as views

experiments_urlpatterns = [
    re_path(
        r'^{}/{}/experiments/{}/stop/?$'.format(USERNAME_PATTERN, NAME_PATTERN, SEQUENCE_PATTERN),
        views.ExperimentStopView.as_view()),
]

urlpatterns = format_suffix_patterns(experiments_urlpatterns)
