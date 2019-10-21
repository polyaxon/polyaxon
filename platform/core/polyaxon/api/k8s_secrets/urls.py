from rest_framework.urlpatterns import format_suffix_patterns

from django.urls import re_path

from api.k8s_secrets import views
from constants.urls import NAME_PATTERN

options_urlpatterns = [
    re_path(r'catalogs/k8s_secrets/?$', views.ClusterK8SSecretListViewV1.as_view()),
    re_path(r'catalogs/k8s_secrets/names?$', views.ClusterK8SSecretNameListView.as_view()),
    re_path(r'catalogs/k8s_secrets/{}/?$'.format(NAME_PATTERN),
            views.ClusterK8SSecretDetailViewV1.as_view()),
]

urlpatterns = format_suffix_patterns(options_urlpatterns)
