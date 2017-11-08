# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from libs.urls import UUID_PATTERN, CLUSTER_UUID_PATTERN, CLUSTER_NODE_UUID_PATTERN
from clusters import views

urlpatterns = [
    url(r'^clusters/?$',
        views.ClusterListView.as_view()),
    url(r'^clusters/{}/?$'.format(UUID_PATTERN),
        views.ClusterDetailView.as_view()),
    url(r'^clusters/{}/nodes/?$'.format(CLUSTER_UUID_PATTERN),
        views.ClusterNodeListView.as_view()),
    url(r'^clusters/{}/nodes/{}/?$'.format(CLUSTER_UUID_PATTERN, UUID_PATTERN),
        views.ClusterNodeDetailView.as_view()),
    url(r'^clusters/{}/nodes/{}/gpus/?$'.format(CLUSTER_UUID_PATTERN, CLUSTER_NODE_UUID_PATTERN),
        views.ClusterNodeGPUListView.as_view()),
    url(r'^clusters/{}/nodes/{}/gpus/{}/?$'.format(CLUSTER_UUID_PATTERN,
                                                   CLUSTER_NODE_UUID_PATTERN,
                                                   UUID_PATTERN),
        views.ClusterNodeGPUDetailView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
