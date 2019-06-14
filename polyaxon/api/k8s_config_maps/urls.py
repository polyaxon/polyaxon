from rest_framework.urlpatterns import format_suffix_patterns

from django.urls import re_path

from api.k8s_config_maps import views
from constants.urls import NAME_PATTERN

options_urlpatterns = [
    re_path(r'catalogs/k8s_config_maps/?$', views.ClusterK8SConfigMapListViewV1.as_view()),
    re_path(r'catalogs/k8s_config_maps/names?$', views.ClusterK8SConfigMapNameListView.as_view()),
    re_path(r'catalogs/k8s_config_maps/{}/?$'.format(NAME_PATTERN),
            views.ClusterK8SConfigMapDetailViewV1.as_view()),
]

urlpatterns = format_suffix_patterns(options_urlpatterns)
