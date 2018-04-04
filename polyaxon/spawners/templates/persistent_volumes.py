import os
from kubernetes import client

from polyaxon_k8s import constants as k8s_constants

from polyaxon_schemas.exceptions import PolyaxonConfigurationError
from polyaxon_schemas.utils import RunTypes, to_list

from spawners.templates import constants


STORAGE_BY_VOLUME = {
    constants.DATA_VOLUME: '1Gi',
    constants.OUTPUTS_VOLUME: '1Gi',
}


def get_host_path_pvol(vol_path):
    return {'host_path': client.V1HostPathVolumeSource(path=vol_path)}


def get_nfs_pvol(vol_path, server=None):
    return {'nfs': client.V1NFSVolumeSource(path=vol_path, server=server)}


def get_persistent_volume_spec(namespace,
                               volume,
                               run_type,
                               access_modes='ReadWriteOnce',
                               persistent_volume_reclaim_policy='Recycle'):
    capacity = {'storage': STORAGE_BY_VOLUME[volume]}
    access_modes = to_list(access_modes)
    vol_path = os.path.join('/', volume)
    if run_type == RunTypes.MINIKUBE:
        params = get_host_path_pvol(vol_path)
    elif run_type == RunTypes.KUBERNETES:
        params = get_nfs_pvol(vol_path)
    else:
        raise PolyaxonConfigurationError('Run type `{}` is not allowed.'.format(run_type))

    volc_name = constants.VOLUME_CLAIM_NAME.format(vol_name=volume)
    claim_ref = client.V1ObjectReference(api_version=k8s_constants.K8S_API_VERSION_V1,
                                         kind=k8s_constants.K8S_PERSISTENT_VOLUME_CLAIM_KIND,
                                         name=volc_name,
                                         namespace=namespace)
    return client.V1PersistentVolumeSpec(
        capacity=capacity,
        access_modes=access_modes,
        persistent_volume_reclaim_policy=persistent_volume_reclaim_policy,
        claim_ref=claim_ref,
        **params)


def get_labels(volume):
    return {'volume': volume}


def get_persistent_volume(namespace, volume, run_type):
    metadata = client.V1ObjectMeta(name=volume, labels=get_labels(volume), namespace=namespace)
    spec = get_persistent_volume_spec(namespace=namespace, volume=volume, run_type=run_type)

    return client.V1PersistentVolume(api_version=k8s_constants.K8S_API_VERSION_V1,
                                     kind=k8s_constants.K8S_PERSISTENT_VOLUME_KIND,
                                     metadata=metadata,
                                     spec=spec)


def get_persistent_volume_claim_spec(volume, access_modes='ReadWriteOnce', ):
    access_modes = to_list(access_modes)
    resources = client.V1ResourceRequirements(requests={'storage': STORAGE_BY_VOLUME[volume]})
    selector = client.V1LabelSelector(match_labels=get_labels(volume))
    return client.V1PersistentVolumeClaimSpec(
        access_modes=access_modes,
        resources=resources,
        selector=selector)


def get_persistent_volume_claim(namespace, volume):
    vol_name = constants.VOLUME_CLAIM_NAME.format(vol_name=volume)
    metadata = client.V1ObjectMeta(name=vol_name, labels=get_labels(volume), namespace=namespace)
    spec = get_persistent_volume_claim_spec(volume)
    return client.V1PersistentVolumeClaim(api_version=k8s_constants.K8S_API_VERSION_V1,
                                          kind=k8s_constants.K8S_PERSISTENT_VOLUME_CLAIM_KIND,
                                          metadata=metadata,
                                          spec=spec)
