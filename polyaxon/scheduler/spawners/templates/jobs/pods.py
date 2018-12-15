import json

from hestia.list_utils import to_list
from kubernetes import client

from django.conf import settings

from constants.k8s_jobs import JOB_NAME_FORMAT
from libs.paths.jobs import get_job_logs_path, get_job_outputs_path
from polyaxon_k8s import constants as k8s_constants
from scheduler.spawners.templates import constants
from scheduler.spawners.templates.env_vars import (
    get_env_var,
    get_job_env_vars,
    get_pod_env_from,
    get_resources_env_vars
)
from scheduler.spawners.templates.gpu_volumes import get_gpu_volumes_def
from scheduler.spawners.templates.init_containers import InitCommands, get_output_args
from scheduler.spawners.templates.pod_environment import (
    get_affinity,
    get_node_selector,
    get_tolerations
)
from scheduler.spawners.templates.resources import get_resources
from scheduler.spawners.templates.sidecars import get_sidecar_args, get_sidecar_container
from scheduler.spawners.templates.volumes import get_pod_outputs_volume
from schemas.exceptions import PolyaxonConfigurationError


class PodManager(object):
    def __init__(self,
                 namespace,
                 name,
                 project_name,
                 project_uuid,
                 job_name,
                 job_uuid,
                 job_docker_image,
                 job_container_name=None,
                 sidecar_container_name=None,
                 sidecar_docker_image=None,
                 sidecar_docker_image_pull_policy=None,
                 init_container_name=None,
                 init_docker_image=None,
                 role_label=None,
                 type_label=None,
                 ports=None,
                 use_sidecar=False,
                 sidecar_config=None,
                 health_check_url=None,
                 log_level=None):
        self.namespace = namespace
        self.name = name
        self.project_name = project_name
        self.project_uuid = project_uuid
        self.job_name = job_name
        self.job_uuid = job_uuid
        self.job_container_name = job_container_name or settings.CONTAINER_NAME_JOB
        self.job_docker_image = job_docker_image
        self.sidecar_container_name = sidecar_container_name or settings.CONTAINER_NAME_SIDECAR
        self.sidecar_docker_image = sidecar_docker_image or settings.JOB_SIDECAR_DOCKER_IMAGE
        self.sidecar_docker_image_pull_policy = (
            sidecar_docker_image_pull_policy or settings.JOB_SIDECAR_DOCKER_IMAGE_PULL_POLICY)
        self.init_container_name = init_container_name or settings.CONTAINER_NAME_INIT
        self.init_docker_image = init_docker_image or settings.JOB_INIT_DOCKER_IMAGE
        self.role_label = role_label or settings.ROLE_LABELS_WORKER
        self.type_label = type_label or settings.TYPE_LABELS_RUNNER
        self.app_label = settings.APP_LABELS_JOB
        self.labels = self.get_labels()
        self.k8s_job_name = self.get_k8s_job_name()
        self.ports = to_list(ports) if ports else []
        self.use_sidecar = use_sidecar
        if use_sidecar and not sidecar_config:
            raise PolyaxonConfigurationError(
                'In order to use a `sidecar_config` is required. '
                'The `sidecar_config` must correspond to the sidecar docker image used.')
        self.sidecar_config = sidecar_config
        self.health_check_url = health_check_url
        self.log_level = log_level

    def get_k8s_job_name(self):
        return JOB_NAME_FORMAT.format(name=self.name, job_uuid=self.job_uuid)

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
                          persistence_outputs,
                          persistence_data,
                          outputs_refs_jobs=None,
                          outputs_refs_experiments=None,
                          secret_refs=None,
                          configmap_refs=None,
                          env_vars=None,
                          command=None,
                          args=None,
                          resources=None):
        """Pod job container for task."""
        # Env vars preparation
        env_vars = to_list(env_vars, check_none=True)
        env_vars += get_job_env_vars(
            log_level=self.log_level,
            persistence_outputs=persistence_outputs,
            outputs_path=get_job_outputs_path(persistence_outputs=persistence_outputs,
                                              job_name=self.job_name),
            persistence_data=persistence_data,
            logs_path=get_job_logs_path(job_name=self.job_name, temp=False),
            outputs_refs_jobs=outputs_refs_jobs,
            outputs_refs_experiments=outputs_refs_experiments
        )
        env_vars += [
            get_env_var(name=constants.CONFIG_MAP_JOB_INFO_KEY_NAME, value=json.dumps(self.labels)),
        ]

        env_vars += get_resources_env_vars(resources=resources)

        # Env from configmap and secret refs
        env_from = get_pod_env_from(secret_refs=secret_refs, configmap_refs=configmap_refs)

        ports = [client.V1ContainerPort(container_port=port) for port in self.ports]
        return client.V1Container(name=self.job_container_name,
                                  image=self.job_docker_image,
                                  command=command,
                                  args=args,
                                  ports=ports or None,
                                  env=env_vars,
                                  env_from=env_from,
                                  resources=get_resources(resources),
                                  volume_mounts=volume_mounts)

    def get_sidecar_container(self):
        """Pod sidecar container for job logs."""
        return get_sidecar_container(
            job_name=self.k8s_job_name,
            job_container_name=self.job_container_name,
            sidecar_container_name=self.sidecar_container_name,
            sidecar_docker_image=self.sidecar_docker_image,
            sidecar_docker_image_pull_policy=self.sidecar_docker_image_pull_policy,
            namespace=self.namespace,
            sidecar_config=self.sidecar_config,
            sidecar_args=get_sidecar_args(pod_id=self.k8s_job_name,
                                          container_id=self.job_container_name,
                                          app_label=self.app_label),
            internal_health_check_url=self.health_check_url)

    def get_init_container(self, persistence_outputs):
        """Pod init container for setting outputs path."""
        outputs_path = get_job_outputs_path(persistence_outputs=persistence_outputs,
                                            job_name=self.job_name)
        _, outputs_volume_mount = get_pod_outputs_volume(persistence_outputs=persistence_outputs)
        return client.V1Container(
            name=self.init_container_name,
            image=self.init_docker_image,
            command=["/bin/sh", "-c"],
            args=to_list(get_output_args(command=InitCommands.CREATE,
                                         outputs_path=outputs_path)),
            volume_mounts=outputs_volume_mount)

    def get_task_pod_spec(self,
                          volume_mounts,
                          volumes,
                          persistence_outputs=None,
                          persistence_data=None,
                          outputs_refs_jobs=None,
                          outputs_refs_experiments=None,
                          env_vars=None,
                          command=None,
                          args=None,
                          resources=None,
                          secret_refs=None,
                          configmap_refs=None,
                          node_selector=None,
                          affinity=None,
                          tolerations=None,
                          restart_policy='OnFailure'):
        """Pod spec to be used to create pods for tasks: master, worker, ps."""
        volume_mounts = to_list(volume_mounts, check_none=True)
        volumes = to_list(volumes, check_none=True)

        gpu_volume_mounts, gpu_volumes = get_gpu_volumes_def(resources)
        volume_mounts += gpu_volume_mounts
        volumes += gpu_volumes

        pod_container = self.get_pod_container(volume_mounts=volume_mounts,
                                               persistence_outputs=persistence_outputs,
                                               persistence_data=persistence_data,
                                               outputs_refs_jobs=outputs_refs_jobs,
                                               outputs_refs_experiments=outputs_refs_experiments,
                                               secret_refs=secret_refs,
                                               configmap_refs=configmap_refs,
                                               env_vars=env_vars,
                                               command=command,
                                               args=args,
                                               resources=resources)

        containers = [pod_container]
        if self.use_sidecar:
            sidecar_container = self.get_sidecar_container()
            containers.append(sidecar_container)

        node_selector = get_node_selector(
            node_selector=node_selector,
            default_node_selector=settings.NODE_SELECTOR_JOBS)
        affinity = get_affinity(
            affinity=affinity,
            default_affinity=settings.AFFINITY_JOBS)
        tolerations = get_tolerations(
            tolerations=tolerations,
            default_tolerations=settings.TOLERATIONS_JOBS)

        service_account_name = None
        if settings.K8S_RBAC_ENABLED and settings.K8S_SERVICE_ACCOUNT_JOBS:
            service_account_name = settings.K8S_SERVICE_ACCOUNT_JOBS
        return client.V1PodSpec(
            restart_policy=restart_policy,
            service_account_name=service_account_name,
            init_containers=to_list(self.get_init_container(persistence_outputs)),
            containers=containers,
            volumes=volumes,
            node_selector=node_selector,
            affinity=affinity,
            tolerations=tolerations)

    def get_pod(self,
                volume_mounts,
                volumes,
                persistence_outputs=None,
                persistence_data=None,
                outputs_refs_jobs=None,
                outputs_refs_experiments=None,
                env_vars=None,
                command=None,
                args=None,
                resources=None,
                secret_refs=None,
                configmap_refs=None,
                node_selector=None,
                affinity=None,
                tolerations=None,
                restart_policy=None):
        metadata = client.V1ObjectMeta(name=self.k8s_job_name,
                                       labels=self.labels,
                                       namespace=self.namespace)

        pod_spec = self.get_task_pod_spec(
            volume_mounts=volume_mounts,
            volumes=volumes,
            persistence_outputs=persistence_outputs,
            persistence_data=persistence_data,
            outputs_refs_jobs=outputs_refs_jobs,
            outputs_refs_experiments=outputs_refs_experiments,
            env_vars=env_vars,
            command=command,
            args=args,
            resources=resources,
            secret_refs=secret_refs,
            configmap_refs=configmap_refs,
            node_selector=node_selector,
            affinity=affinity,
            tolerations=tolerations,
            restart_policy=restart_policy)
        return client.V1Pod(api_version=k8s_constants.K8S_API_VERSION_V1,
                            kind=k8s_constants.K8S_POD_KIND,
                            metadata=metadata,
                            spec=pod_spec)
