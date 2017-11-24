# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from kubernetes import client

from polyaxon_schemas.utils import TaskType

from polyaxon_k8s import constants as k8s_constants

from polyaxon_spawner.templates import constants
from polyaxon_spawner.templates.persistent_volumes import get_vol_path


def get_cluster_env_var(project, experiment, task_type):
    cluster_name = constants.CONFIG_MAP_NAME.format(project=project,
                                                    experiment=experiment,
                                                    role='cluster')
    config_map_key_ref = client.V1ConfigMapKeySelector(name=cluster_name, key=task_type)
    value = client.V1EnvVarSource(config_map_key_ref=config_map_key_ref)
    key_name = constants.CONFIG_MAP_KEY_NAME.format(project=project.replace('-', '_'),
                                                    experiment=experiment,
                                                    role='cluster',
                                                    task_type=task_type)
    return client.V1EnvVar(name=key_name, value_from=value)


def get_resources(resources):
    limits = {}
    requests = {}
    if resources is None:
        return None
    if resources.cpu:
        if resources.cpu.limits:
            limits['cpu'] = resources.memory.limits
        if resources.cpu.request:
            limits['cpu'] = resources.memory.request

    if resources.cpu:
        if resources.cpu.limits:
            limits['memory'] = resources.memory.limits
        if resources.cpu.request:
            limits['memory'] = resources.memory.request

    if resources.gpu:
        if resources.gpu.limits:
            limits['alpha.kubernetes.io/nvidia-gpu'] = resources.gpu.limits
        if resources.cpu.request:
            limits['alpha.kubernetes.io/nvidia-gpu'] = resources.gpu.request
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


def get_volume_mount(volume, run_type):
    volume_name = constants.VOLUME_NAME.format(vol_name=volume)
    return client.V1VolumeMount(name=volume_name,
                                mount_path=get_vol_path(volume, run_type))


def get_volume(volume):
    vol_name = constants.VOLUME_NAME.format(vol_name=volume)
    volc_name = constants.VOLUME_CLAIM_NAME.format(vol_name=volume)
    pv_claim = client.V1PersistentVolumeClaimVolumeSource(claim_name=volc_name)
    return client.V1Volume(name=vol_name, persistent_volume_claim=pv_claim)


def get_project_pod_spec(project,
                         name,
                         volume_mounts,
                         volumes,
                         command=None,
                         args=None,
                         ports=None,
                         resources=None,
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
                                     image=constants.DOCKER_JOB_IMAGE,
                                     command=command,
                                     args=args,
                                     ports=ports,
                                     env=env_vars,
                                     resources=get_resources(resources),
                                     volume_mounts=volume_mounts)]
    return client.V1PodSpec(restart_policy=restart_policy, containers=containers, volumes=volumes)


def get_pod_container(project,
                      experiment,
                      task_type,
                      task_id,
                      volume_mounts,
                      env_vars=None,
                      command=None,
                      args=None,
                      ports=None,
                      resources=None):
    env_vars = env_vars or []
    env_vars += [
        get_cluster_env_var(project=project,
                            experiment=experiment,
                            task_type=TaskType.MASTER),
        get_cluster_env_var(project=project,
                            experiment=experiment,
                            task_type=TaskType.WORKER),
        get_cluster_env_var(project=project,
                            experiment=experiment,
                            task_type=TaskType.PS),
    ]

    ports = [client.V1ContainerPort(container_port=port) for port in ports]
    return client.V1Container(name=constants.POD_CONTAINER_JOB_NAME,
                              image=constants.DOCKER_JOB_IMAGE,
                              command=command,
                              args=args,
                              ports=ports,
                              env=env_vars,
                              resources=get_resources(resources),
                              volume_mounts=volume_mounts)


def get_sidecar_container(namespace,
                          project,
                          experiment,
                          task_type,
                          task_id,
                          amqp_url,
                          log_routing_key,
                          internal_exchange=None,
                          resources=None):
    task_name = constants.TASK_NAME.format(project=project,
                                           experiment=experiment,
                                           task_type=task_type,
                                           task_id=task_id)

    env_vars = [
        client.V1EnvVar(name='POLYAXON_K8S_NAMESPACE', value=namespace),
        client.V1EnvVar(name='POLYAXON_POD_ID', value=task_name),
        client.V1EnvVar(name='POLYAXON_JOB_ID', value=constants.POD_CONTAINER_JOB_NAME),
        client.V1EnvVar(name='POLYAXON_AMQP_URL', value=amqp_url),
        client.V1EnvVar(name='POLYAXON_LOG_ROUTING_KEY', value=log_routing_key),
        client.V1EnvVar(name='POLYAXON_INTERNAL_EXCHANGE', value=internal_exchange),
    ]
    return client.V1Container(name=constants.POD_CONTAINER_SIDECAR_NAME,
                              image=constants.DOCKER_SIDECAR_IMAGE,
                              env=env_vars,
                              resources=resources)


def get_task_pod_spec(namespace,
                      project,
                      experiment,
                      task_type,
                      task_id,
                      volume_mounts,
                      volumes,
                      env_vars=None,
                      command=None,
                      args=None,
                      ports=None,
                      resources=None,
                      use_sidecar=False,
                      log_routing_key=None,
                      internal_exchange=None,
                      amqp_url=None,
                      restart_policy='OnFailure'):
    """Pod spec to be used to create pods for tasks: master, worker, ps."""
    volume_mounts = volume_mounts or []
    volumes = volumes or []

    # volume_mounts += get_gpu_volume_mounts()
    # volumes += get_gpu_volumes()

    pod_container = get_pod_container(project=project,
                                      experiment=experiment,
                                      task_type=task_type,
                                      task_id=task_id,
                                      volume_mounts=volume_mounts,
                                      env_vars=env_vars,
                                      command=command,
                                      args=args,
                                      ports=ports,
                                      resources=resources)

    containers = [pod_container]
    if use_sidecar:
        assert amqp_url, '`amqp_url` is required'
        assert log_routing_key, '`log_routing_key` is required'
        sidecar_container = get_sidecar_container(namespace=namespace,
                                                  project=project,
                                                  experiment=experiment,
                                                  task_type=task_type,
                                                  task_id=task_id,
                                                  amqp_url=amqp_url,
                                                  log_routing_key=log_routing_key,
                                                  internal_exchange=internal_exchange,
                                                  resources=resources)
        containers.append(sidecar_container)
    return client.V1PodSpec(restart_policy=restart_policy, containers=containers, volumes=volumes)


def get_labels(project, experiment, task_type, task_id, task_name):
    return {'project': project,
            'experiment': '{}'.format(experiment),
            'task_type': task_type,
            'task_id': '{}'.format(task_id),
            'task': task_name,
            'role': constants.WORKER_ROLE_LABEL,
            'type': constants.EXPERIMENT_TYPE_LABEL}


def get_pod(namespace,
            project,
            experiment,
            task_type,
            task_id,
            volume_mounts,
            volumes,
            ports,
            command=None,
            args=None,
            resources=None,
            use_sidecar=False,
            amqp_url=None,
            log_routing_key=None,
            internal_exchange=None,
            restart_policy=None):
    task_name = constants.TASK_NAME.format(project=project,
                                           experiment=experiment,
                                           task_type=task_type,
                                           task_id=task_id)
    labels = get_labels(project=project,
                        experiment=experiment,
                        task_type=task_type,
                        task_id=task_id,
                        task_name=task_name)
    metadata = client.V1ObjectMeta(name=task_name, labels=labels, namespace=namespace)

    pod_spec = get_task_pod_spec(namespace=namespace,
                                 project=project,
                                 experiment=experiment,
                                 task_type=task_type,
                                 task_id=task_id,
                                 volume_mounts=volume_mounts,
                                 volumes=volumes,
                                 command=command,
                                 args=args,
                                 ports=ports,
                                 resources=resources,
                                 restart_policy=restart_policy,
                                 use_sidecar=use_sidecar,
                                 amqp_url=amqp_url,
                                 log_routing_key=log_routing_key,
                                 internal_exchange=internal_exchange)
    return client.V1Pod(api_version=k8s_constants.K8S_API_VERSION_V1,
                        kind=k8s_constants.K8S_POD_KIND,
                        metadata=metadata,
                        spec=pod_spec)
