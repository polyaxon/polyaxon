# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import os

from kubernetes import client

from polyaxon_schemas.exceptions import PolyaxonConfigurationError
from polyaxon_schemas.k8s.templates import constants
from polyaxon_schemas.settings import RunTypes
from polyaxon_schemas.utils import to_list

STORAGE_BY_VOLUME = {
    constants.DATA_VOLUME: '1Gi',
    constants.LOGS_VOLUME: '1Mi',
    constants.TMP_VOLUME: '1Ki'
}


def get_host_path_pvol(volume):
    vol_path = os.path.join('/', volume)
    return {'host_path': client.V1HostPathVolumeSource(path=vol_path)}


def get_nfs_pvol(volume, server=None):
    vol_path = os.path.join('/', volume)
    return {'nfs': client.V1NFSVolumeSource(path=vol_path, server=server)}


def get_persistent_volume_spec(volume,
                               run_type,
                               access_modes='ReadWriteOnce',
                               persistent_volume_reclaim_policy='Recycle'):
    capacity = {'storage': STORAGE_BY_VOLUME[volume]}
    access_modes = to_list(access_modes)
    if run_type == RunTypes.MINIKUBE:
        params = get_host_path_pvol(volume)
    elif run_type == RunTypes.KUBERNETES:
        params = get_nfs_pvol(volume)
    else:
        raise PolyaxonConfigurationError('Run type `{}` is not allowed.'.format(run_type))

    return client.V1PersistentVolumeSpec(
        capacity=capacity,
        access_modes=access_modes,
        persistent_volume_reclaim_policy=persistent_volume_reclaim_policy,
        **params)


def get_persistent_volume(volume, run_type):
    vol_name = constants.VOLUME_NAME.format(vol_name=volume)
    metadata = client.V1ObjectMeta(name=vol_name)
    spec = get_persistent_volume_spec(volume, run_type)

    return client.V1PersistentVolume(api_version=constants.K8S_API_VERSION_V1,
                                     kind=constants.K8S_PERSISTENT_VOLUME_KIND,
                                     metadata=metadata,
                                     spec=spec)


def get_persistent_volume_claim_spec(volume, access_modes='ReadWriteOnce', ):
    access_modes = to_list(access_modes)
    resources = client.V1ResourceRequirements(requests={'storage': STORAGE_BY_VOLUME[volume]})
    return client.V1PersistentVolumeClaimSpec(
        access_modes=access_modes,
        resources=resources)


def get_persistent_volume_claim(volume):
    vol_name = constants.VOLUME_NAME.format(vol_name=volume)
    metadata = client.V1ObjectMeta(name=vol_name)
    spec = get_persistent_volume_claim_spec(volume)
    return client.V1PersistentVolumeClaim(api_version=constants.K8S_API_VERSION_V1,
                                          kind=constants.K8S_PERSISTENT_VOLUME_CLAIM_KIND,
                                          metadata=metadata,
                                          spec=spec)
