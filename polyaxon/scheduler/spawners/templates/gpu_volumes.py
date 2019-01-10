from kubernetes import client

import conf


def get_gpu_volumes():
    return [
        client.V1Volume(
            name='nvidia-bin',
            host_path=client.V1HostPathVolumeSource(path=conf.get('DIRS_NVIDIA').get('bin'))),
        client.V1Volume(
            name='nvidia-lib',
            host_path=client.V1HostPathVolumeSource(path=conf.get('DIRS_NVIDIA').get('lib'))),
        client.V1Volume(
            name='nvidia-libcuda',
            host_path=client.V1HostPathVolumeSource(path=conf.get('DIRS_NVIDIA').get('libcuda'))),
    ]


def get_gpu_volume_mounts():
    return [
        client.V1VolumeMount(name='nvidia-bin',
                             mount_path=conf.get('MOUNT_PATHS_NVIDIA').get('bin')),
        client.V1VolumeMount(name='nvidia-lib',
                             mount_path=conf.get('MOUNT_PATHS_NVIDIA').get('lib')),
        client.V1VolumeMount(name='nvidia-libcuda',
                             mount_path=conf.get('MOUNT_PATHS_NVIDIA').get('libcuda')),
    ]


def get_gpu_volumes_def(resources):
    volume_mounts = []
    volumes = []
    if resources and resources.gpu and (conf.get('DIRS_NVIDIA') and conf.get('MOUNT_PATHS_NVIDIA')):
        volume_mounts = get_gpu_volume_mounts()
        volumes = get_gpu_volumes()

    return volume_mounts, volumes
