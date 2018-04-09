from django.conf import settings

from spawners.templates import constants, pods


def get_pod_volumes():
    volumes = []
    volume_mounts = []
    volumes.append(pods.get_volume(volume=constants.DATA_VOLUME,
                                   claim_name=settings.DATA_CLAIM_NAME,
                                   volume_mount=settings.DATA_ROOT))
    volume_mounts.append(pods.get_volume_mount(volume=constants.DATA_VOLUME,
                                               volume_mount=settings.DATA_ROOT))

    volumes.append(pods.get_volume(volume=constants.OUTPUTS_VOLUME,
                                   claim_name=settings.OUTPUTS_CLAIM_NAME,
                                   volume_mount=settings.OUTPUTS_ROOT))
    volume_mounts.append(pods.get_volume_mount(volume=constants.OUTPUTS_VOLUME,
                                               volume_mount=settings.OUTPUTS_ROOT))
    return volumes, volume_mounts
