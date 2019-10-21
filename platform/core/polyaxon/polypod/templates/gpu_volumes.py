from kubernetes import client

import conf

from options.registry.mount_paths import DIRS_NVIDIA, MOUNT_PATHS_NVIDIA


def get_gpu_volumes():
    dirs_nvidia = conf.get(DIRS_NVIDIA)
    return [
        client.V1Volume(
            name='nvidia-bin',
            host_path=client.V1HostPathVolumeSource(path=dirs_nvidia.get('bin'))),
        client.V1Volume(
            name='nvidia-lib',
            host_path=client.V1HostPathVolumeSource(path=dirs_nvidia.get('lib'))),
        client.V1Volume(
            name='nvidia-libcuda',
            host_path=client.V1HostPathVolumeSource(path=dirs_nvidia.get('libcuda'))),
    ]


def get_gpu_volume_mounts():
    mount_paths_nvidia = conf.get(MOUNT_PATHS_NVIDIA)
    return [
        client.V1VolumeMount(name='nvidia-bin',
                             mount_path=mount_paths_nvidia.get('bin')),
        client.V1VolumeMount(name='nvidia-lib',
                             mount_path=mount_paths_nvidia.get('lib')),
        client.V1VolumeMount(name='nvidia-libcuda',
                             mount_path=mount_paths_nvidia.get('libcuda')),
    ]


def get_gpu_volumes_def(resources):
    volume_mounts = []
    volumes = []
    if resources and resources.gpu and (conf.get(DIRS_NVIDIA) and conf.get(MOUNT_PATHS_NVIDIA)):
        volume_mounts = get_gpu_volume_mounts()
        volumes = get_gpu_volumes()

    return volume_mounts, volumes
