from rest_framework.urlpatterns import format_suffix_patterns

from django.urls import re_path

from api.data_stores import views
from constants.urls import NAME_PATTERN

options_urlpatterns = [
    re_path(r'catalogs/data_stores/?$', views.DataStoreListViewV1.as_view()),
    re_path(r'catalogs/data_stores/names?$', views.DataStoreNameListView.as_view()),
    re_path(r'catalogs/data_stores/{}/?$'.format(NAME_PATTERN),
            views.DataStoreDetailViewV1.as_view()),
]

urlpatterns = format_suffix_patterns(options_urlpatterns)
