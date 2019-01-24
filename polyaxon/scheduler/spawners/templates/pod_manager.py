from hestia.list_utils import to_list
from kubernetes import client
from polyaxon_k8s import constants as k8s_constants

from scheduler.spawners.templates.env_vars import (
    get_job_env_vars,
    get_pod_env_from,
    get_resources_env_vars
)
from scheduler.spawners.templates.gpu_volumes import get_gpu_volumes_def
from scheduler.spawners.templates.resources import get_resources
from scheduler.spawners.templates.sidecars import get_sidecar_container, get_sidecar_args
from schemas.exceptions import PolyaxonConfigurationError


class BasePodManager(object):
    def __init__(self,
                 namespace,
                 project_name,
                 project_uuid,
                 job_container_name,
                 job_docker_image,
                 sidecar_container_name,
                 sidecar_docker_image,
                 sidecar_docker_image_pull_policy,
                 init_container_name,
                 init_docker_image,
                 role_label,
                 type_label,
                 app_label,
                 ports,
                 health_check_url,
                 use_sidecar,
                 sidecar_config,
                 log_level):
        self.namespace = namespace
        self.project_name = project_name
        self.project_uuid = project_uuid
        self.job_container_name = job_container_name
        self.job_docker_image = job_docker_image
        self.sidecar_container_name = sidecar_container_name
        self.sidecar_docker_image = sidecar_docker_image
        self.sidecar_docker_image_pull_policy = sidecar_docker_image_pull_policy
        self.init_container_name = init_container_name
        self.init_docker_image = init_docker_image
        self.role_label = role_label
        self.type_label = type_label
        self.app_label = app_label
        self.ports = ports
        self.use_sidecar = use_sidecar
        if use_sidecar and not sidecar_config:
            raise PolyaxonConfigurationError(
                'In order to use a `sidecar_config` is required. '
                'The `sidecar_config` must correspond to the sidecar docker image used.')
        self.sidecar_config = sidecar_config
        self.health_check_url = health_check_url
        self.log_level = log_level

    def get_job_name(self, **kwargs):
        raise NotImplementedError()

    def get_labels(self):
        raise NotImplementedError()

    def _pod_container_checks(self):
        pass

    def _get_logs_path(self, persistence_logs='default'):
        raise NotImplementedError()

    def _get_outputs_path(self, persistence_outputs):
        raise NotImplementedError()

    def _get_container_pod_env_vars(self):
        raise NotImplementedError()

    def get_pod_container(self,
                          volume_mounts,
                          persistence_outputs=None,
                          persistence_data=None,
                          outputs_refs_jobs=None,
                          outputs_refs_experiments=None,
                          secret_refs=None,
                          configmap_refs=None,
                          env_vars=None,
                          command=None,
                          args=None,
                          resources=None,
                          ephemeral_token=None):
        """Pod job container for task."""
        self._pod_container_checks()

        # Env vars preparations
        env_vars = to_list(env_vars, check_none=True)
        logs_path = self._get_logs_path()
        outputs_path = self._get_outputs_path(persistence_outputs=persistence_outputs)
        env_vars += get_job_env_vars(
            persistence_outputs=persistence_outputs,
            outputs_path=outputs_path,
            persistence_data=persistence_data,
            log_level=self.log_level,
            logs_path=logs_path,
            outputs_refs_jobs=outputs_refs_jobs,
            outputs_refs_experiments=outputs_refs_experiments,
            ephemeral_token=ephemeral_token,
        )
        env_vars += self._get_container_pod_env_vars()
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

    def get_sidecar_container(self, job_name):
        """Pod sidecar container for task logs."""
        return get_sidecar_container(
            job_name=job_name,
            job_container_name=self.job_container_name,
            sidecar_container_name=self.sidecar_container_name,
            sidecar_docker_image=self.sidecar_docker_image,
            sidecar_docker_image_pull_policy=self.sidecar_docker_image_pull_policy,
            namespace=self.namespace,
            sidecar_config=self.sidecar_config,
            sidecar_args=get_sidecar_args(pod_id=job_name,
                                          container_id=self.job_container_name,
                                          app_label=self.app_label),
            internal_health_check_url=self.health_check_url)

    def get_init_container(self, persistence_outputs):
        """Pod init container for setting outputs path."""
        raise NotImplementedError()

    def get_task_pod_spec(self,
                          volume_mounts,
                          volumes,
                          job_name,
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
                          ephemeral_token=None,
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
                                               resources=resources,
                                               env_vars=env_vars,
                                               command=command,
                                               args=args,
                                               ephemeral_token=ephemeral_token)

        containers = [pod_container]
        if self.use_sidecar:
            sidecar_container = self.get_sidecar_container(job_name=job_name)
            containers.append(sidecar_container)

        node_selector = self._get_node_selector(node_selector=node_selector)
        affinity = self._get_affinity(affinity=affinity)
        tolerations = self._get_tolerations(tolerations=tolerations)
        service_account_name = self._get_service_account_name()
        return client.V1PodSpec(
            restart_policy=restart_policy,
            service_account_name=service_account_name,
            init_containers=to_list(self.get_init_container(persistence_outputs)),
            containers=containers,
            volumes=volumes,
            node_selector=node_selector,
            tolerations=tolerations,
            affinity=affinity)

    def _get_node_selector(self, node_selector):
        raise NotImplementedError()

    def _get_affinity(self, affinity):
        raise NotImplementedError()

    def _get_tolerations(self, tolerations):
        raise NotImplementedError()

    def _get_service_account_name(self):
        raise NotImplementedError()

    def get_pod(self,
                job_name,
                volume_mounts,
                volumes,
                labels,
                env_vars=None,
                command=None,
                args=None,
                persistence_outputs=None,
                persistence_data=None,
                outputs_refs_jobs=None,
                outputs_refs_experiments=None,
                secret_refs=None,
                configmap_refs=None,
                resources=None,
                ephemeral_token=None,
                node_selector=None,
                affinity=None,
                tolerations=None,
                restart_policy=None):
        metadata = client.V1ObjectMeta(name=job_name, labels=labels, namespace=self.namespace)

        pod_spec = self.get_task_pod_spec(
            job_name=job_name,
            volume_mounts=volume_mounts,
            volumes=volumes,
            env_vars=env_vars,
            command=command,
            args=args,
            persistence_outputs=persistence_outputs,
            persistence_data=persistence_data,
            outputs_refs_jobs=outputs_refs_jobs,
            outputs_refs_experiments=outputs_refs_experiments,
            secret_refs=secret_refs,
            configmap_refs=configmap_refs,
            resources=resources,
            ephemeral_token=ephemeral_token,
            node_selector=node_selector,
            affinity=affinity,
            tolerations=tolerations,
            restart_policy=restart_policy)
        return client.V1Pod(api_version=k8s_constants.K8S_API_VERSION_V1,
                            kind=k8s_constants.K8S_POD_KIND,
                            metadata=metadata,
                            spec=pod_spec)
