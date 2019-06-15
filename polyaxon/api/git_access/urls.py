from rest_framework.urlpatterns import format_suffix_patterns

from django.urls import re_path

from api.git_access import views
from constants.urls import NAME_PATTERN

options_urlpatterns = [
    re_path(r'catalogs/git_access/?$', views.GitAccessListViewV1.as_view()),
    re_path(r'catalogs/git_access/names?$', views.GitAccessNameListView.as_view()),
    re_path(r'catalogs/git_access/{}/?$'.format(NAME_PATTERN),
            views.GitAccessDetailViewV1.as_view()),
]

urlpatterns = format_suffix_patterns(options_urlpatterns)
