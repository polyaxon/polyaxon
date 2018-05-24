from rest_framework.urlpatterns import format_suffix_patterns

from django.urls import re_path

from apis.clusters import views

clusters_urlpatterns = [
    re_path(r'^cluster/?$',
            views.ClusterDetailView.as_view())
]

urlpatterns = format_suffix_patterns(clusters_urlpatterns)
