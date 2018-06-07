import json

from kubernetes import client

from django.conf import settings

from libs.paths.jobs import get_job_outputs_path, get_job_logs_path, get_job_data_path
from libs.paths.projects import get_project_data_path
from libs.utils import get_list
from polyaxon_k8s import constants as k8s_constants
from polyaxon_schemas.exceptions import PolyaxonConfigurationError
from scheduler.spawners.templates import constants
from scheduler.spawners.templates.env_vars import (
    get_env_var,
    get_service_env_vars,
    get_job_env_vars, get_resources_env_vars)
from scheduler.spawners.templates.gpu_volumes import get_gpu_volumes_def
from scheduler.spawners.templates.resources import get_resources
from scheduler.spawners.templates.sidecar import get_sidecar_command, get_sidecar_args


class PodManager(object):
    def __init__(self,
                 namespace,
                 project_name,
                 project_uuid,
                 job_name,
                 job_uuid,
                 job_docker_image,
                 job_container_name=None,
                 sidecar_container_name=None,
                 sidecar_docker_image=None,
                 role_label=None,
                 type_label=None,
                 ports=None,
                 use_sidecar=False,
                 sidecar_config=None,
                 log_level=None):
        self.namespace = namespace
        self.project_name = project_name
        self.project_uuid = project_uuid
        self.job_name = job_name
        self.job_uuid = job_uuid
        self.job_container_name = job_container_name or settings.CONTAINER_NAME_JOB
        self.job_docker_image = job_docker_image
        self.sidecar_container_name = sidecar_container_name or settings.CONTAINER_NAME_SIDECAR
        self.sidecar_docker_image = sidecar_docker_image or settings.JOB_SIDECAR_DOCKER_IMAGE
        self.role_label = role_label or settings.ROLE_LABELS_WORKER
        self.type_label = type_label or settings.TYPE_LABELS_EXPERIMENT
        self.app_label = settings.APP_LABELS_JOB
        self.labels = self.get_labels()
        self.pod_name = self.get_job_name()
        self.ports = ports
        self.use_sidecar = use_sidecar
        if use_sidecar and not sidecar_config:
            raise PolyaxonConfigurationError(
                'In order to use a `sidecar_config` is required. '
                'The `sidecar_config` must correspond to the sidecar docker image used.')
        self.sidecar_config = sidecar_config
        self.log_level = log_level

    def get_job_name(self):
        return constants.JOB_NAME.format(name=settings.APP_LABELS_JOB, job_uuid=self.job_uuid)

    def get_labels(self):
        labels = {
            'project_name': self.project_name,
            'project_uuid': self.project_uuid,
            'job_name': self.job_name,
            'job_uuid': self.job_uuid,
            'role': self.role_label,
            'type': self.type_label,
            'app': self.app_label
        }
        return labels

    def get_pod_container(self,
                          volume_mounts,
                          env_vars=None,
                          command=None,
                          args=None,
                          resources=None):
        """Pod job container for task."""
        env_vars = get_list(env_vars)
        env_vars += get_job_env_vars(
            log_level=self.log_level,
            outputs_path=get_job_outputs_path(job_name=self.job_name),
            logs_path=get_job_logs_path(job_name=self.job_name),
            data_path=get_job_data_path(job_name=self.job_name),
            project_data_path=get_project_data_path(project_name=self.project_name)
        )
        env_vars += [
            get_env_var(name=constants.CONFIG_MAP_JOB_INFO_KEY_NAME, value=json.dumps(self.labels)),
        ]

        if resources:
            env_vars += get_resources_env_vars(resources=resources)

        ports = [client.V1ContainerPort(container_port=port) for port in self.ports]
        return client.V1Container(name=self.job_container_name,
                                  image=self.job_docker_image,
                                  command=command,
                                  args=args,
                                  ports=ports,
                                  env=env_vars,
                                  resources=get_resources(resources),
                                  volume_mounts=volume_mounts)

    def get_sidecar_container(self):
        """Pod sidecar container for task logs."""
        env_vars = [
            client.V1EnvVar(name='POLYAXON_POD_ID', value=self.job_name),
            client.V1EnvVar(name='POLYAXON_JOB_ID', value=self.job_container_name),
        ]
        env_vars += get_service_env_vars(namespace=self.namespace)
        for k, v in self.sidecar_config.items():
            env_vars.append(client.V1EnvVar(name=k, value=v))
        return client.V1Container(name=self.sidecar_container_name,
                                  image=self.sidecar_docker_image,
                                  command=get_sidecar_command(app_label=self.app_label),
                                  env=env_vars,
                                  args=get_sidecar_args(pod_id=self.pod_name))

    def get_task_pod_spec(self,
                          volume_mounts,
                          volumes,
                          env_vars=None,
                          command=None,
                          args=None,
                          resources=None,
                          node_selector=None,
                          restart_policy='OnFailure'):
        """Pod spec to be used to create pods for tasks: master, worker, ps."""
        volume_mounts = get_list(volume_mounts)
        volumes = get_list(volumes)

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
            sidecar_container = self.get_sidecar_container()
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

    def get_pod(self,
                volume_mounts,
                volumes,
                env_vars=None,
                command=None,
                args=None,
                resources=None,
                node_selector=None,
                restart_policy=None):
        metadata = client.V1ObjectMeta(name=self.job_name,
                                       labels=self.labels,
                                       namespace=self.namespace)

        pod_spec = self.get_task_pod_spec(
            volume_mounts=volume_mounts,
            volumes=volumes,
            env_vars=env_vars,
            command=command,
            args=args,
            resources=resources,
            node_selector=node_selector,
            restart_policy=restart_policy)
        return client.V1Pod(api_version=k8s_constants.K8S_API_VERSION_V1,
                            kind=k8s_constants.K8S_POD_KIND,
                            metadata=metadata,
                            spec=pod_spec)
