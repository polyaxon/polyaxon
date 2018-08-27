from rest_framework.urlpatterns import format_suffix_patterns

from django.urls import re_path

from api.searches import views
from constants.urls import ID_PATTERN, NAME_PATTERN, USERNAME_PATTERN

searches_urlpatterns = [
    re_path(r'^searches/{}/{}/groups/?$'.format(USERNAME_PATTERN, NAME_PATTERN),
            views.ExperimentGroupSearchListView.as_view()),
    re_path(r'^searches/{}/{}/experiments/?$'.format(USERNAME_PATTERN, NAME_PATTERN),
            views.ExperimentSearchListView.as_view()),
    re_path(r'^searches/{}/{}/builds/?$'.format(USERNAME_PATTERN, NAME_PATTERN),
            views.BuildSearchListView.as_view()),
    re_path(r'^searches/{}/{}/jobs/?$'.format(USERNAME_PATTERN, NAME_PATTERN),
            views.JobSearchListView.as_view()),

    re_path(r'^searches/{}/{}/groups/{}?$'.format(USERNAME_PATTERN, NAME_PATTERN, ID_PATTERN),
            views.ExperimentGroupSearchDeleteView.as_view()),
    re_path(r'^searches/{}/{}/experiments/{}?$'.format(USERNAME_PATTERN, NAME_PATTERN, ID_PATTERN),
            views.ExperimentSearchDeleteView.as_view()),
    re_path(r'^searches/{}/{}/builds/{}?$'.format(USERNAME_PATTERN, NAME_PATTERN, ID_PATTERN),
            views.BuildSearchDeleteView.as_view()),
    re_path(r'^searches/{}/{}/jobs/{}?$'.format(USERNAME_PATTERN, NAME_PATTERN, ID_PATTERN),
            views.JobSearchDeleteView.as_view()),
]

urlpatterns = format_suffix_patterns(searches_urlpatterns)
