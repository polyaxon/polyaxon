from rest_framework.urlpatterns import format_suffix_patterns

from django.urls import re_path

from api.data_stores import views
from constants.urls import UUID_PATTERN

options_urlpatterns = [
    re_path(r'catalogs/data_stores/?$', views.DataStoreListViewV1.as_view()),
    re_path(r'catalogs/data_stores/{}/?$'.format(UUID_PATTERN),
            views.DataStoreDetailViewV1.as_view()),
]

urlpatterns = format_suffix_patterns(options_urlpatterns)
