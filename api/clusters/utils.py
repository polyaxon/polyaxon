# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from django.conf import settings
from django.contrib.auth import get_user_model

from clusters.models import Cluster


def get_cluster():
    if settings.CLUSTER_ID:
        cluster = Cluster.objects.get(uuid=settings.CLUSTER_ID)
    else:
        # Get default cluster
        cluster = Cluster.objects.first()

    if cluster:
        return cluster

    cluster = Cluster.objects.create(user=get_user_model().objects.first(), version_api={})
    return cluster
