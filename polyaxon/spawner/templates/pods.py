# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import json

import six
import uuid

from django.conf import settings
from kubernetes import client

from polyaxon_schemas.exceptions import PolyaxonConfigurationError

from polyaxon_k8s import constants as k8s_constants

from spawner.templates import constants


def get_gpu_volume_mounts():
    return [
        client.V1VolumeMount(name='nvidia-bin',
                             mount_path=settings.MOUNT_PATHS_NVIDIA.get('bin')),
        client.V1VolumeMount(name='nvidia-lib',
                             mount_path=settings.MOUNT_PATHS_NVIDIA.get('lib')),
        client.V1VolumeMount(name='nvidia-libcuda',
                             mount_path=settings.MOUNT_PATHS_NVIDIA.get('libcuda')),
    ]


def get_gpu_volumes():
    return [
        client.V1Volume(
            name='nvidia-bin',
            host_path=client.V1HostPathVolumeSource(path=settings.DIRS_NVIDIA.get('bin'))),
        client.V1Volume(
            name='nvidia-lib',
            host_path=client.V1HostPathVolumeSource(path=settings.DIRS_NVIDIA.get('lib'))),
        client.V1Volume(
            name='nvidia-libcuda',
            host_path=client.V1HostPathVolumeSource(path=settings.DIRS_NVIDIA.get('libcuda'))),
    ]


def get_gpu_volumes_def(resources):
    volume_mounts = []
    volumes = []
    if resources and resources.gpu and (settings.DIRS_NVIDIA and settings.MOUNT_PATHS_NVIDIA):
        volume_mounts = get_gpu_volume_mounts()
        volumes = get_gpu_volumes()

    return volume_mounts, volumes


def get_volume_mount(volume, volume_mount=None):
    return client.V1VolumeMount(name=volume, mount_path=volume_mount)


def get_volume(volume, claim_name=None, volume_mount=None):
    if claim_name:
        pv_claim = client.V1PersistentVolumeClaimVolumeSource(claim_name=claim_name)
        return client.V1Volume(name=volume, persistent_volume_claim=pv_claim)
    elif volume_mount:
        return client.V1Volume(
            name=volume,
            host_path=client.V1HostPathVolumeSource(path=volume_mount))
    else:
        empty_dir = client.V1EmptyDirVolumeSource()
        return client.V1Volume(name=volume, empty_dir=empty_dir)


def get_resources(resources):
    """Create resources requirements.

    Args:
        resources: `PodResourcesConfig`

    Return:
        `V1ResourceRequirements`
    """
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
            limits['memory'] = '{}Mi'.format(resources.memory.limits)
        if resources.cpu.request:
            limits['memory'] = '{}Mi'.format(resources.memory.request)

    if resources.gpu:
        if resources.gpu.limits:
            limits['alpha.kubernetes.io/nvidia-gpu'] = resources.gpu.limits
        if resources.gpu.request:
            limits['alpha.kubernetes.io/nvidia-gpu'] = resources.gpu.request
    return client.V1ResourceRequirements(limits=limits, requests=requests)


class PodManager(object):
    def __init__(self,
                 namespace,
                 project_name,
                 experiment_group_name,
                 experiment_name,
                 project_uuid,
                 experiment_group_uuid,
                 experiment_uuid,
                 job_container_name=None,
                 job_docker_image=None,
                 sidecar_container_name=None,
                 sidecar_docker_image=None,
                 role_label=None,
                 type_label=None,
                 ports=None,
                 use_sidecar=False,
                 sidecar_config=None):
        self.namespace = namespace
        self.project_name = project_name
        self.experiment_group_name = experiment_group_name
        self.experiment_name = experiment_name
        self.project_uuid = project_uuid
        self.experiment_group_uuid = experiment_group_uuid
        self.experiment_uuid = experiment_uuid
        self.job_container_name = job_container_name or settings.JOB_CONTAINER_NAME
        self.job_docker_image = job_docker_image or settings.JOB_DOCKER_NAME
        self.sidecar_container_name = sidecar_container_name or settings.JOB_SIDECAR_CONTAINER_NAME
        self.sidecar_docker_image = sidecar_docker_image or settings.JOB_SIDECAR_DOCKER_IMAGE
        self.role_label = role_label or settings.ROLE_LABELS_WORKER
        self.type_label = type_label or settings.TYPE_LABELS_EXPERIMENT
        self.ports = ports or [constants.DEFAULT_PORT]
        self.use_sidecar = use_sidecar
        if use_sidecar and not sidecar_config:
            raise PolyaxonConfigurationError(
                'In order to use a `sidecar_config` is required. '
                'The `sidecar_config` must correspond to the sidecar docker image used.')
        self.sidecar_config = sidecar_config

    def get_job_name(self, task_type, task_idx):
        return constants.JOB_NAME.format(task_type=task_type,
                                         task_idx=task_idx,
                                         experiment_uuid=self.experiment_uuid)

    def get_job_uuid(self, task_type, task_idx):
        name = self.get_job_name(task_type, task_idx)
        return uuid.uuid5(uuid.NAMESPACE_DNS, name).hex

    def get_from_experiment_config_map(self, key_name):
        name = constants.CONFIG_MAP_NAME.format(experiment_uuid=self.experiment_uuid)
        config_map_key_ref = client.V1ConfigMapKeySelector(name=name, key=key_name)
        value = client.V1EnvVarSource(config_map_key_ref=config_map_key_ref)
        return client.V1EnvVar(name=key_name, value_from=value)

    def get_from_experiment_secret(self, key_name):
        name = constants.SECRET_NAME.format(experiment_uuid=self.experiment_uuid)
        secret_key_ref = client.V1SecretKeySelector(name=name, key=key_name)
        value = client.V1EnvVarSource(secret_key_ref=secret_key_ref)
        return client.V1EnvVar(name=key_name, value_from=value)

    @staticmethod
    def get_from_app_secret(key_name, key):
        secret_key_ref = client.V1SecretKeySelector(name=settings.POLYAXON_K8S_APP_SECRET_NAME,
                                                    key=key)
        value = client.V1EnvVarSource(secret_key_ref=secret_key_ref)
        return client.V1EnvVar(name=key_name, value_from=value)

    def get_pod_container(self,
                          volume_mounts,
                          env_vars=None,
                          command=None,
                          args=None,
                          resources=None):
        """Pod job container for task."""
        env_vars = env_vars or []
        env_vars += [
            self.get_from_experiment_config_map(constants.CONFIG_MAP_CLUSTER_KEY_NAME),
            self.get_from_experiment_config_map(constants.CONFIG_MAP_DECLARATIONS_KEY_NAME),
            self.get_from_experiment_config_map(constants.CONFIG_MAP_EXPERIMENT_INFO_KEY_NAME),
            self.get_from_experiment_config_map(constants.CONFIG_MAP_LOG_LEVEL_KEY_NAME),
            self.get_from_experiment_config_map(constants.CONFIG_MAP_API_KEY_NAME),
            self.get_from_experiment_config_map(
                constants.CONFIG_MAP_EXPERIMENT_OUTPUTS_PATH_KEY_NAME),
            self.get_from_experiment_secret(constants.SECRET_USER_TOKEN),
        ]

        ports = [client.V1ContainerPort(container_port=port) for port in self.ports]
        return client.V1Container(name=self.job_container_name,
                                  image=self.job_docker_image,
                                  command=command,
                                  args=args,
                                  ports=ports,
                                  env=env_vars,
                                  resources=get_resources(resources),
                                  volume_mounts=volume_mounts)

    def get_sidecar_container(self, task_type, task_idx, args, resources=None):
        """Pod sidecar container for task logs."""
        job_name = self.get_job_name(task_type=task_type, task_idx=task_idx)

        env_vars = [
            client.V1EnvVar(name='POLYAXON_K8S_NAMESPACE', value=self.namespace),
            client.V1EnvVar(name='POLYAXON_POD_ID', value=job_name),
            client.V1EnvVar(name='POLYAXON_JOB_ID', value=self.job_container_name),
            self.get_from_app_secret('POLYAXON_SECRET_KEY', 'polyaxon-secret')
        ]
        for k, v in six.iteritems(self.sidecar_config):
            env_vars.append(client.V1EnvVar(name=k, value=v))
        return client.V1Container(name=self.sidecar_container_name,
                                  image=self.sidecar_docker_image,
                                  env=env_vars,
                                  args=args,
                                  resources=resources)

    def get_task_pod_spec(self,
                          task_type,
                          task_idx,
                          volume_mounts,
                          volumes,
                          env_vars=None,
                          command=None,
                          args=None,
                          sidecar_args=None,
                          resources=None,
                          restart_policy='OnFailure'):
        """Pod spec to be used to create pods for tasks: master, worker, ps."""
        volume_mounts = volume_mounts or []
        volumes = volumes or []

        gpu_volume_mounts, gpu_volumes = get_gpu_volumes_def(resources)
        volume_mounts += gpu_volume_mounts
        volumes += gpu_volumes

        pod_container = self.get_pod_container(volume_mounts=volume_mounts,
                                               env_vars=env_vars,
                                               command=command,
                                               args=args,
                                               resources=resources)

        containers = [pod_container]
        if self.use_sidecar:
            sidecar_container = self.get_sidecar_container(task_type=task_type,
                                                           task_idx=task_idx,
                                                           args=sidecar_args,
                                                           resources=resources)
            containers.append(sidecar_container)

        node_selector = settings.NODE_SELECTORS_EXPERIMENTS
        node_selector = json.loads(node_selector) if node_selector else None
        service_account_name = None
        if settings.K8S_RBAC_ENABLED:
            service_account_name = settings.K8S_SERVICE_ACCOUNT_NAME
        return client.V1PodSpec(restart_policy=restart_policy,
                                service_account_name=service_account_name,
                                containers=containers,
                                volumes=volumes,
                                node_selector=node_selector)

    def get_labels(self, task_type, task_idx):
        labels = {'project_name': self.project_name,
                  'experiment_group_name': self.experiment_group_name,
                  'experiment_name': self.experiment_name,
                  'project_uuid': self.project_uuid,
                  'experiment_uuid': self.experiment_uuid,
                  'task_type': task_type,
                  'task_idx': '{}'.format(task_idx),
                  'job_uuid': self.get_job_uuid(task_type, task_idx),
                  'role': self.role_label,
                  'type': self.type_label}
        if self.experiment_group_uuid:
            labels['experiment_group_uuid'] = self.experiment_group_uuid
        return labels

    def get_pod(self,
                task_type,
                task_idx,
                volume_mounts,
                volumes,
                command=None,
                args=None,
                sidecar_args=None,
                resources=None,
                restart_policy=None):
        job_name = self.get_job_name(task_type=task_type, task_idx=task_idx)
        labels = self.get_labels(task_type=task_type, task_idx=task_idx)
        metadata = client.V1ObjectMeta(name=job_name, labels=labels, namespace=self.namespace)

        pod_spec = self.get_task_pod_spec(
            task_type=task_type,
            task_idx=task_idx,
            volume_mounts=volume_mounts,
            volumes=volumes,
            command=command,
            args=args,
            sidecar_args=sidecar_args,
            resources=resources,
            restart_policy=restart_policy)
        return client.V1Pod(api_version=k8s_constants.K8S_API_VERSION_V1,
                            kind=k8s_constants.K8S_POD_KIND,
                            metadata=metadata,
                            spec=pod_spec)
