import json
import logging
import uuid

from kubernetes import client

from django.conf import settings

from libs.api import API_KEY_NAME
from libs.utils import get_list
from polyaxon_k8s import constants as k8s_constants
from polyaxon_schemas.exceptions import PolyaxonConfigurationError
from scheduler.spawners.templates import constants
from scheduler.spawners.templates.env_vars import get_from_app_secret
from scheduler.spawners.templates.gpu_volumes import get_gpu_volumes_def
from scheduler.spawners.templates.resources import get_resources
from scheduler.spawners.templates.internal_services_env_vars import get_service_env_vars

logger = logging.getLogger('polyaxon.spawners.spawners')


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
        self.job_container_name = job_container_name or settings.CONTAINER_NAME_JOB
        self.job_docker_image = job_docker_image or settings.JOB_DOCKER_NAME
        self.sidecar_container_name = sidecar_container_name or settings.CONTAINER_NAME_SIDECAR
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

    def get_pod_container(self,
                          volume_mounts,
                          env_vars=None,
                          command=None,
                          args=None,
                          resources=None):
        """Pod job container for task."""
        env_vars = get_list(env_vars)
        env_vars += [
            self.get_from_experiment_config_map(constants.CONFIG_MAP_CLUSTER_KEY_NAME),
            self.get_from_experiment_config_map(constants.CONFIG_MAP_DECLARATIONS_KEY_NAME),
            self.get_from_experiment_config_map(constants.CONFIG_MAP_EXPERIMENT_INFO_KEY_NAME),
            self.get_from_experiment_config_map(constants.CONFIG_MAP_LOG_LEVEL_KEY_NAME),
            self.get_from_experiment_config_map(API_KEY_NAME),
            self.get_from_experiment_config_map(
                constants.CONFIG_MAP_EXPERIMENT_OUTPUTS_PATH_KEY_NAME),
            self.get_from_experiment_config_map(
                constants.CONFIG_MAP_EXPERIMENT_LOGS_PATH_KEY_NAME),
            self.get_from_experiment_config_map(
                constants.CONFIG_MAP_EXPERIMENT_DATA_PATH_KEY_NAME),
            get_from_app_secret('POLYAXON_SECRET_KEY', 'polyaxon-secret'),
            get_from_app_secret('POLYAXON_INTERNAL_SECRET_TOKEN', 'polyaxon-internal-secret-token')
        ]

        if resources:
            if resources.gpu and settings.LD_LIBRARY_PATH:
                env_vars.append(client.V1EnvVar(name='LD_LIBRARY_PATH',
                                                value=settings.LD_LIBRARY_PATH))
            if resources.gpu and not settings.LD_LIBRARY_PATH:
                logger.warning('`LD_LIBRARY_PATH` was not properly set.')  # Publish error

        ports = [client.V1ContainerPort(container_port=port) for port in self.ports]
        return client.V1Container(name=self.job_container_name,
                                  image=self.job_docker_image,
                                  command=command,
                                  args=args,
                                  ports=ports,
                                  env=env_vars,
                                  resources=get_resources(resources),
                                  volume_mounts=volume_mounts)

    def get_sidecar_container(self, task_type, task_idx, args):
        """Pod sidecar container for task logs."""
        job_name = self.get_job_name(task_type=task_type, task_idx=task_idx)

        env_vars = [
            client.V1EnvVar(name='POLYAXON_K8S_NAMESPACE', value=self.namespace),
            client.V1EnvVar(name='POLYAXON_POD_ID', value=job_name),
            client.V1EnvVar(name='POLYAXON_JOB_ID', value=self.job_container_name),
        ]
        env_vars += get_service_env_vars()
        for k, v in self.sidecar_config.items():
            env_vars.append(client.V1EnvVar(name=k, value=v))
        return client.V1Container(name=self.sidecar_container_name,
                                  image=self.sidecar_docker_image,
                                  env=env_vars,
                                  args=args)

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
                          node_selector=None,
                          restart_policy='OnFailure'):
        """Pod spec to be used to create pods for tasks: master, worker, ps."""
        volume_mounts = get_list(volume_mounts)
        volumes = get_list(volumes)

        gpu_volume_mounts, gpu_volumes = get_gpu_volumes_def(resources)
        volume_mounts += gpu_volume_mounts
        volumes += gpu_volumes

        # Add job information
        env_vars = get_list(env_vars)
        env_vars.append(
            client.V1EnvVar(
                name=constants.CONFIG_MAP_TASK_INFO_KEY_NAME,
                value=json.dumps({'type': task_type, 'index': task_idx})
            )
        )

        pod_container = self.get_pod_container(volume_mounts=volume_mounts,
                                               env_vars=env_vars,
                                               command=command,
                                               args=args,
                                               resources=resources)

        containers = [pod_container]
        if self.use_sidecar:
            sidecar_container = self.get_sidecar_container(task_type=task_type,
                                                           task_idx=task_idx,
                                                           args=sidecar_args)
            containers.append(sidecar_container)

        if not node_selector:
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
                  'job_uuid': uuid.uuid4().hex,
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
                env_vars=None,
                command=None,
                args=None,
                sidecar_args=None,
                resources=None,
                node_selector=None,
                restart_policy=None):
        job_name = self.get_job_name(task_type=task_type, task_idx=task_idx)
        labels = self.get_labels(task_type=task_type, task_idx=task_idx)
        metadata = client.V1ObjectMeta(name=job_name, labels=labels, namespace=self.namespace)

        pod_spec = self.get_task_pod_spec(
            task_type=task_type,
            task_idx=task_idx,
            volume_mounts=volume_mounts,
            volumes=volumes,
            env_vars=env_vars,
            command=command,
            args=args,
            sidecar_args=sidecar_args,
            resources=resources,
            node_selector=node_selector,
            restart_policy=restart_policy)
        return client.V1Pod(api_version=k8s_constants.K8S_API_VERSION_V1,
                            kind=k8s_constants.K8S_POD_KIND,
                            metadata=metadata,
                            spec=pod_spec)
