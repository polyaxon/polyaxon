from django.conf import settings

from runner.spawners.templates import constants, pods


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

    if settings.EXTRA_PERSISTENCES:
        for i, extra_data in enumerate(settings.EXTRA_PERSISTENCES):
            volume_name = 'extra-{}'.format(i)
            mount_path = extra_data.get('mountPath')
            claim_name = extra_data.get('existingClaim')
            host_path = extra_data.get('hostPath')
            if mount_path:
                volumes.append(pods.get_volume(volume=volume_name,
                                               claim_name=claim_name,
                                               volume_mount=host_path))
                volume_mounts.append(pods.get_volume_mount(volume=volume_name,
                                                           volume_mount=mount_path))
    return volumes, volume_mounts
