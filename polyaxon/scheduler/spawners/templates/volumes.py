from kubernetes import client

from django.conf import settings

from libs.paths.data_paths import validate_persistence_data
from libs.paths.exceptions import VolumeNotFoundError
from libs.paths.outputs_paths import validate_persistence_outputs
from scheduler.spawners.templates import constants


def get_volume_mount(volume, volume_mount=None, read_only=False):
    return client.V1VolumeMount(name=volume, mount_path=volume_mount, read_only=read_only)


def get_volume(volume, claim_name=None, host_path=None):
    if claim_name:
        pv_claim = client.V1PersistentVolumeClaimVolumeSource(claim_name=claim_name)
        return client.V1Volume(name=volume, persistent_volume_claim=pv_claim)

    if host_path:
        return client.V1Volume(
            name=volume,
            host_path=client.V1HostPathVolumeSource(path=host_path))

    empty_dir = client.V1EmptyDirVolumeSource()
    return client.V1Volume(name=volume, empty_dir=empty_dir)


def get_volume_from_definition(volume_name, volume_settings):
    if volume_name not in volume_settings:
        raise VolumeNotFoundError('Volume with name `{}` was defined in specification, '
                                  'but was not found'.format(volume_name))
    volumes = []
    volume_mounts = []
    definition = volume_settings[volume_name]
    mount_path = definition.get('mountPath')
    claim_name = definition.get('existingClaim')
    host_path = definition.get('hostPath')
    read_only = definition.get('readOnly', False)
    if mount_path:
        volumes.append(get_volume(volume=volume_name,
                                  claim_name=claim_name,
                                  host_path=host_path))
        volume_mounts.append(get_volume_mount(volume=volume_name,
                                              volume_mount=mount_path,
                                              read_only=read_only))

    return volumes, volume_mounts


def get_pod_data_volume(persistence_data):
    persistence_data = validate_persistence_data(persistence_data=persistence_data)
    volumes = []
    volume_mounts = []
    for persistence_name in persistence_data:
        persistence_volumes, persistence_volume_mounts = get_volume_from_definition(
            volume_name=persistence_name,
            volume_settings=settings.PERSISTENCE_DATA)
        volumes += persistence_volumes
        volume_mounts += persistence_volume_mounts
    return volumes, volume_mounts


def get_pod_outputs_volume(persistence_outputs):
    persistence_outputs = validate_persistence_outputs(persistence_outputs=persistence_outputs)
    return get_volume_from_definition(volume_name=persistence_outputs,
                                      volume_settings=settings.PERSISTENCE_OUTPUTS)


def get_pod_refs_outputs_volumes(outputs_refs, persistence_outputs):
    volumes, volume_mounts = [], []

    if not outputs_refs:
        return volumes, volume_mounts

    persistences = set([ref.persistence for ref in outputs_refs if ref != persistence_outputs])
    for persistence in persistences:
        p_volumes, p_volume_mounts = get_volume_from_definition(
            volume_name=persistence,
            volume_settings=settings.PERSISTENCE_OUTPUTS)
        volumes.append(p_volumes)
        volume_mounts.append(p_volume_mounts)

    return volumes, volume_mounts


def get_pod_volumes(persistence_outputs, persistence_data):
    outputs_volumes, outputs_volume_mounts = get_pod_outputs_volume(persistence_outputs)
    data_volumes, data_volume_mounts = get_pod_data_volume(persistence_data)
    volumes = outputs_volumes + data_volumes
    volume_mounts = outputs_volume_mounts + data_volume_mounts
    return volumes, volume_mounts


def get_docker_volumes():
    volumes = [get_volume(volume=constants.DOCKER_VOLUME, host_path=settings.MOUNT_PATHS_DOCKER)]
    volume_mounts = [get_volume_mount(volume=constants.DOCKER_VOLUME,
                                      volume_mount=settings.MOUNT_PATHS_DOCKER)]
    return volumes, volume_mounts
