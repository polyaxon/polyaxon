# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from kubernetes import client

from polyaxon_schemas.exceptions import PolyaxonConfigurationError
from polyaxon_schemas.polyaxonfile.utils import get_vol_path
from polyaxon_schemas.utils import RunTypes, to_list

from polyaxon_k8s.k8s.templates import constants


STORAGE_BY_VOLUME = {
    constants.DATA_VOLUME: '1Gi',
    constants.POLYAXON_FILES_VOLUME: '1Mi',
    constants.LOGS_VOLUME: '1Mi',
}


def get_host_path_pvol(vol_path):
    return {'host_path': client.V1HostPathVolumeSource(path=vol_path)}


def get_nfs_pvol(vol_path, server=None):
    return {'nfs': client.V1NFSVolumeSource(path=vol_path, server=server)}


def get_persistent_volume_spec(project,
                               volume,
                               run_type,
                               namespace,
                               access_modes='ReadWriteOnce',
                               persistent_volume_reclaim_policy='Recycle'):
    capacity = {'storage': STORAGE_BY_VOLUME[volume]}
    access_modes = to_list(access_modes)
    vol_path = get_vol_path(project, volume, run_type)
    if run_type == RunTypes.MINIKUBE:
        params = get_host_path_pvol(vol_path)
    elif run_type == RunTypes.KUBERNETES:
        params = get_nfs_pvol(vol_path)
    else:
        raise PolyaxonConfigurationError('Run type `{}` is not allowed.'.format(run_type))

    volc_name = constants.VOLUME_CLAIM_NAME.format(project=project, vol_name=volume)
    claim_ref = client.V1ObjectReference(api_version=constants.K8S_API_VERSION_V1,
                                         kind=constants.K8S_PERSISTENT_VOLUME_CLAIM_KIND,
                                         name=volc_name,
                                         namespace=namespace)
    return client.V1PersistentVolumeSpec(
        capacity=capacity,
        access_modes=access_modes,
        persistent_volume_reclaim_policy=persistent_volume_reclaim_policy,
        claim_ref=claim_ref,
        **params)


def get_labels(project, volume):
    return {'project': project, 'volume': volume}


def get_persistent_volume(project, volume, run_type, namespace):
    vol_name = constants.VOLUME_NAME.format(project=project, vol_name=volume)
    metadata = client.V1ObjectMeta(name=vol_name, labels=get_labels(project, volume))
    spec = get_persistent_volume_spec(project, volume, run_type, namespace)

    return client.V1PersistentVolume(api_version=constants.K8S_API_VERSION_V1,
                                     kind=constants.K8S_PERSISTENT_VOLUME_KIND,
                                     metadata=metadata,
                                     spec=spec)


def get_persistent_volume_claim_spec(project, volume, access_modes='ReadWriteOnce', ):
    access_modes = to_list(access_modes)
    resources = client.V1ResourceRequirements(requests={'storage': STORAGE_BY_VOLUME[volume]})
    selector = client.V1LabelSelector(match_labels=get_labels(project, volume))
    return client.V1PersistentVolumeClaimSpec(
        access_modes=access_modes,
        resources=resources,
        selector=selector)


def get_persistent_volume_claim(project, volume):
    vol_name = constants.VOLUME_CLAIM_NAME.format(project=project, vol_name=volume)
    metadata = client.V1ObjectMeta(name=vol_name, labels=get_labels(project, volume))
    spec = get_persistent_volume_claim_spec(project, volume)
    return client.V1PersistentVolumeClaim(api_version=constants.K8S_API_VERSION_V1,
                                          kind=constants.K8S_PERSISTENT_VOLUME_CLAIM_KIND,
                                          metadata=metadata,
                                          spec=spec)
