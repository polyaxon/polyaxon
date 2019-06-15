from rest_framework.urlpatterns import format_suffix_patterns

from django.urls import re_path

from api.registry_access import views
from constants.urls import NAME_PATTERN

options_urlpatterns = [
    re_path(r'catalogs/registry_access/?$', views.RegistryAccessListViewV1.as_view()),
    re_path(r'catalogs/registry_access/names?$', views.RegistryAccessNameListView.as_view()),
    re_path(r'catalogs/registry_access/{}/?$'.format(NAME_PATTERN),
            views.RegistryAccessDetailViewV1.as_view()),
]

urlpatterns = format_suffix_patterns(options_urlpatterns)
