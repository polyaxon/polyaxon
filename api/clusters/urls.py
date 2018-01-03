# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from libs.urls import UUID_PATTERN, CLUSTER_NODE_UUID_PATTERN
from clusters import views

clusters_urlpatterns = [
    url(r'^cluster/?$',
        views.ClusterDetailView.as_view()),
    url(r'^cluster/nodes/?$',
        views.ClusterNodeListView.as_view()),
]

cluster_nodes_urlpatterns = [
    url(r'^nodes/{}/?$'.format(UUID_PATTERN),
        views.ClusterNodeDetailView.as_view()),
    url(r'^nodes/{}/gpus/?$'.format(CLUSTER_NODE_UUID_PATTERN),
        views.ClusterNodeGPUListView.as_view()),
    url(r'^nodes/{}/gpus/{}/?$'.format(CLUSTER_NODE_UUID_PATTERN, UUID_PATTERN),
        views.ClusterNodeGPUDetailView.as_view()),
]

urlpatterns = format_suffix_patterns(clusters_urlpatterns + cluster_nodes_urlpatterns)
