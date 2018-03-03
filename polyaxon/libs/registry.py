# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from django.conf import settings

from polyaxon_k8s.manager import K8SManager


def get_registry_host():
    if not hasattr(settings, 'REGISTRY_HOST'):
        k8s = K8SManager(namespace=settings.K8S_NAMESPACE, in_cluster=True)
        settings.REGISTRY_HOST = '{}:{}'.format(
            k8s.get_service(name=settings.REGISTRY_HOST_NAME).spec.cluster_ip,
            settings.REGISTRY_PORT)

    return settings.REGISTRY_HOST
