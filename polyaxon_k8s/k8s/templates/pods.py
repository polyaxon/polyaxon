# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from kubernetes import client

from polyaxon_schemas.utils import TaskType

from polyaxon_k8s.k8s.templates import constants
from polyaxon_k8s.k8s.templates.persistent_volumes import get_vol_path


class PodStatus(object):
    RUNNING = 'Running'
    PENDING = 'Pending'
    CONTAINER_CREATING = 'ContainerCreating'
    SUCCEEDED = 'Succeeded'
    FAILED = 'Failed'


def get_cluster_env_var(project, experiment, task_type):
    cluster_name = constants.CONFIG_MAP_CLUSTER_NAME.format(project=project, experiment=experiment)
    config_map_key_ref = client.V1ConfigMapKeySelector(name=cluster_name, key=task_type)
    value = client.V1EnvVarSource(config_map_key_ref=config_map_key_ref)
    key_name = constants.CONFIG_MAP_CLUSTER_KEY_NAME.format(project=project,
                                                            experiment=experiment,
                                                            task_type=task_type)
    return client.V1EnvVar(name=key_name, value_from=value)


def get_gpu_resources(gpu_limits=0, gpu_requests=0):
    limits = constants.GPU_RESOURCES.format(gpu_limits) if gpu_limits > 0 else None
    requests = constants.GPU_RESOURCES.format(gpu_requests) if gpu_requests > 0 else None
    return client.V1ResourceRequirements(limits=limits, requests=requests)


def get_gpu_volume_mounts():
    return [
        client.V1VolumeMount(name='bin', mount_path='/usr/local/nvidia/bin'),
        client.V1VolumeMount(name='lib', mount_path='/usr/local/nvidia/lib'),
    ]


def get_gpu_volumes():
    return [
        client.V1Volume(name='bin',
                        host_path=client.V1HostPathVolumeSource(path='/usr/local/nvidia/bin')),
        client.V1Volume(name='lib',
                        host_path=client.V1HostPathVolumeSource(path='/usr/local/nvidia/lib')),
    ]


def get_volume_mount(project, volume, run_type):
    volume_name = constants.VOLUME_NAME.format(project=project, vol_name=volume)
    return client.V1VolumeMount(name=volume_name,
                                mount_path=get_vol_path(project, volume, run_type))


def get_volume(project, volume):
    vol_name = constants.VOLUME_NAME.format(project=project, vol_name=volume)
    volc_name = constants.VOLUME_CLAIM_NAME.format(project=project, vol_name=volume)
    pv_claim = client.V1PersistentVolumeClaimVolumeSource(claim_name=volc_name)
    return client.V1Volume(name=vol_name, persistent_volume_claim=pv_claim)


def get_project_pod_spec(project,
                         name,
                         volume_mounts,
                         volumes,
                         command=None,
                         args=None,
                         ports=None,
                         gpu_limits=0,
                         gpu_requests=0,
                         env_vars=None,
                         restart_policy=None):
    """Pod spec to be used to create pods for project side: tensorboard, notebooks."""
    volume_mounts = volume_mounts or []
    volumes = volumes or []

    volume_mounts = volume_mounts or []
    volumes = volumes or []

    # volume_mounts += get_gpu_volume_mounts()
    # volumes += get_gpu_volumes()

    ports = [client.V1ContainerPort(container_port=port) for port in ports]

    container_name = constants.POD_CONTAINER_PROJECT_NAME.format(project=project, name=name)
    containers = [client.V1Container(name=container_name,
                                     image=constants.DOCKER_IMAGE,
                                     command=command,
                                     args=args,
                                     ports=ports,
                                     env=env_vars,
                                     resources=get_gpu_resources(gpu_limits, gpu_requests),
                                     volume_mounts=volume_mounts)]
    return client.V1PodSpec(restart_policy=restart_policy, containers=containers, volumes=volumes)


def get_task_pod_spec(project,
                      experiment,
                      task_type,
                      task_id,
                      volume_mounts,
                      volumes,
                      env_vars=None,
                      command=None,
                      args=None,
                      ports=None,
                      gpu_limits=0,
                      gpu_requests=0,
                      restart_policy='OnFailure'):
    """Pod spec to be used to create pods for tasks: master, worker, ps."""
    env_vars = env_vars or []
    env_vars += [
        get_cluster_env_var(project=project, experiment=experiment, task_type=TaskType.MASTER),
        get_cluster_env_var(project=project, experiment=experiment, task_type=TaskType.WORKER),
        get_cluster_env_var(project=project, experiment=experiment, task_type=TaskType.PS),
    ]

    volume_mounts = volume_mounts or []
    volumes = volumes or []

    # volume_mounts += get_gpu_volume_mounts()
    # volumes += get_gpu_volumes()

    ports = [client.V1ContainerPort(container_port=port) for port in ports]

    container_name = constants.POD_CONTAINER_TASK_NAME.format(project=project,
                                                              experiment=experiment,
                                                              task_type=task_type,
                                                              task_id=task_id)
    containers = [client.V1Container(name=container_name,
                                     image=constants.DOCKER_IMAGE,
                                     command=command,
                                     args=args,
                                     ports=ports,
                                     env=env_vars,
                                     resources=get_gpu_resources(gpu_limits, gpu_requests),
                                     volume_mounts=volume_mounts)]
    return client.V1PodSpec(restart_policy=restart_policy, containers=containers, volumes=volumes)


def get_labels(project, experiment, task_type, task_id, task_name):
    return {'project': project,
            'experiment': '{}'.format(experiment),
            'task_type': task_type,
            'task_id': '{}'.format(task_id),
            'task': task_name}


def get_pod(project,
            experiment,
            task_type,
            task_id,
            volume_mounts,
            volumes,
            ports,
            command=None,
            args=None,
            restart_policy=None):
    task_name = constants.TASK_NAME.format(project=project,
                                           experiment=experiment,
                                           task_type=task_type,
                                           task_id=task_id)
    labels = get_labels(project, experiment, task_type, task_id, task_name)
    metadata = client.V1ObjectMeta(name=task_name, labels=labels)

    spec = get_task_pod_spec(project=project,
                             experiment=experiment,
                             task_type=task_type,
                             task_id=task_id,
                             volume_mounts=volume_mounts,
                             volumes=volumes,
                             command=command,
                             args=args,
                             ports=ports,
                             restart_policy=restart_policy)
    return client.V1Pod(api_version=constants.K8S_API_VERSION_V1,
                        kind=constants.K8S_POD_KIND,
                        metadata=metadata,
                        spec=spec)
