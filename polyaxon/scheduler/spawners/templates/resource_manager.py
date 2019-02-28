from collections import Mapping

from hestia.list_utils import to_list
from kubernetes import client

from polyaxon_k8s import constants as k8s_constants
from scheduler.spawners.templates.env_vars import get_pod_env_from, get_resources_env_vars
from scheduler.spawners.templates.gpu_volumes import get_gpu_volumes_def
from scheduler.spawners.templates.resources import get_resources
from scheduler.spawners.templates.sidecars import get_sidecar_args, get_sidecar_container
from scheduler.spawners.templates.tpu import get_tpu_annotations, requests_tpu
from schemas.exceptions import PolyaxonConfigurationError


class BaseResourceManager(object):
    def __init__(self,
                 namespace,
                 project_name,
                 project_uuid,
                 job_container_name,
                 job_docker_image,
                 job_docker_image_pull_policy,
                 sidecar_container_name,
                 sidecar_docker_image,
                 sidecar_docker_image_pull_policy,
                 init_container_name,
                 init_docker_image,
                 init_docker_image_pull_policy,
                 role_label,
                 type_label,
                 app_label,
                 health_check_url,
                 use_sidecar,
                 sidecar_config,
                 log_level):
        self.namespace = namespace
        self.project_name = project_name
        self.project_uuid = project_uuid
        self.job_container_name = job_container_name
        self.job_docker_image = job_docker_image
        self.job_docker_image_pull_policy = job_docker_image_pull_policy
        self.sidecar_container_name = sidecar_container_name
        self.sidecar_docker_image = sidecar_docker_image
        self.sidecar_docker_image_pull_policy = sidecar_docker_image_pull_policy
        self.init_container_name = init_container_name
        self.init_docker_image = init_docker_image
        self.init_docker_image_pull_policy = init_docker_image_pull_policy
        self.role_label = role_label
        self.type_label = type_label
        self.app_label = app_label
        self.use_sidecar = use_sidecar
        if use_sidecar and not sidecar_config:
            sidecar_config = {}
        if use_sidecar and not isinstance(sidecar_config, Mapping):
            raise PolyaxonConfigurationError(
                'In order to use a `sidecar_config` is required. '
                'The `sidecar_config` must correspond to the sidecar docker image used.')
        self.sidecar_config = sidecar_config
        self.health_check_url = health_check_url
        self.log_level = log_level

    def get_resource_name(self):
        raise NotImplementedError()

    def get_labels(self):
        raise NotImplementedError()

    def _pod_container_checks(self):
        pass

    def _get_logs_path(self, persistence_logs='default'):
        raise NotImplementedError()

    def _get_outputs_path(self, persistence_outputs):
        raise NotImplementedError()

    def _get_container_pod_env_vars(self,
                                    persistence_outputs,
                                    persistence_data,
                                    outputs_refs_jobs,
                                    outputs_refs_experiments,
                                    ephemeral_token):
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
                          ports=None,
                          ephemeral_token=None):
        """Pod job container for task."""
        self._pod_container_checks()

        # Env vars preparations
        env_vars = to_list(env_vars, check_none=True)
        env_vars += self._get_container_pod_env_vars(
            persistence_outputs=persistence_outputs,
            persistence_data=persistence_data,
            outputs_refs_jobs=outputs_refs_jobs,
            outputs_refs_experiments=outputs_refs_experiments,
            ephemeral_token=ephemeral_token
        )
        env_vars += get_resources_env_vars(resources=resources)

        # Env from configmap and secret refs
        env_from = get_pod_env_from(secret_refs=secret_refs, configmap_refs=configmap_refs)

        def get_ports():
            _ports = to_list(ports) if ports else []
            return [client.V1ContainerPort(container_port=port) for port in _ports] or None

        return client.V1Container(name=self.job_container_name,
                                  image=self.job_docker_image,
                                  command=command,
                                  args=args,
                                  ports=get_ports(),
                                  env=env_vars,
                                  env_from=env_from,
                                  resources=get_resources(resources),
                                  volume_mounts=volume_mounts)

    def get_sidecar_volume_mounts(self, context_mounts, persistence_outputs, persistence_data):
        return context_mounts

    def get_sidecar_container(self, resource_name, volume_mounts):
        """Pod sidecar container for task logs."""
        return get_sidecar_container(
            resource_name=resource_name,
            job_container_name=self.job_container_name,
            sidecar_container_name=self.sidecar_container_name,
            sidecar_docker_image=self.sidecar_docker_image,
            sidecar_docker_image_pull_policy=self.sidecar_docker_image_pull_policy,
            namespace=self.namespace,
            sidecar_config=self.sidecar_config,
            sidecar_args=get_sidecar_args(pod_id=resource_name,
                                          container_id=self.job_container_name,
                                          app_label=self.app_label),
            internal_health_check_url=self.health_check_url,
            volume_mounts=volume_mounts)

    def get_init_container(self,
                           init_command,
                           init_args,
                           env_vars,
                           context_mounts,
                           persistence_outputs,
                           persistence_data):
        """Pod init container for setting outputs path."""
        raise NotImplementedError()

    def get_task_pod_spec(self,
                          volume_mounts,
                          volumes,
                          resource_name,
                          persistence_outputs=None,
                          persistence_data=None,
                          outputs_refs_jobs=None,
                          outputs_refs_experiments=None,
                          env_vars=None,
                          command=None,
                          args=None,
                          init_command=None,
                          init_args=None,
                          init_env_vars=None,
                          resources=None,
                          ports=None,
                          secret_refs=None,
                          configmap_refs=None,
                          ephemeral_token=None,
                          node_selector=None,
                          affinity=None,
                          tolerations=None,
                          sidecar_context_mounts=None,
                          init_context_mounts=None,
                          restart_policy='OnFailure'):
        """Pod spec to be used to create pods for tasks: master, worker, ps."""
        sidecar_context_mounts = to_list(sidecar_context_mounts, check_none=True)
        init_context_mounts = to_list(init_context_mounts, check_none=True)
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
                                               ports=ports,
                                               ephemeral_token=ephemeral_token)

        containers = [pod_container]
        if self.use_sidecar:
            sidecar_volume_mounts = self.get_sidecar_volume_mounts(
                persistence_outputs=persistence_outputs,
                persistence_data=persistence_data,
                context_mounts=sidecar_context_mounts)
            sidecar_container = self.get_sidecar_container(resource_name=resource_name,
                                                           volume_mounts=sidecar_volume_mounts)
            containers.append(sidecar_container)

        init_container = self.get_init_container(init_command=init_command,
                                                 init_args=init_args,
                                                 env_vars=init_env_vars,
                                                 context_mounts=init_context_mounts,
                                                 persistence_outputs=persistence_outputs,
                                                 persistence_data=persistence_data)
        init_containers = to_list(init_container, check_none=True)

        node_selector = self._get_node_selector(node_selector=node_selector)
        affinity = self._get_affinity(affinity=affinity)
        tolerations = self._get_tolerations(tolerations=tolerations)
        service_account_name = self._get_service_account_name()
        return client.V1PodSpec(
            restart_policy=restart_policy,
            service_account_name=service_account_name,
            init_containers=init_containers,
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
                resource_name,
                volume_mounts,
                volumes,
                labels,
                env_vars=None,
                command=None,
                args=None,
                init_command=None,
                init_args=None,
                init_env_vars=None,
                ports=None,
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
                sidecar_context_mounts=None,
                init_context_mounts=None,
                restart_policy=None):
        annotations = None
        if requests_tpu(resources):
            annotations = get_tpu_annotations()
        metadata = client.V1ObjectMeta(name=resource_name,
                                       labels=labels,
                                       namespace=self.namespace,
                                       annotations=annotations)

        pod_spec = self.get_task_pod_spec(
            resource_name=resource_name,
            volume_mounts=volume_mounts,
            volumes=volumes,
            env_vars=env_vars,
            command=command,
            args=args,
            init_command=init_command,
            init_args=init_args,
            init_env_vars=init_env_vars,
            ports=ports,
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
            init_context_mounts=init_context_mounts,
            sidecar_context_mounts=sidecar_context_mounts,
            restart_policy=restart_policy)
        return client.V1Pod(api_version=k8s_constants.K8S_API_VERSION_V1,
                            kind=k8s_constants.K8S_POD_KIND,
                            metadata=metadata,
                            spec=pod_spec)

    def get_deployment_spec(self,
                            resource_name,
                            volume_mounts,
                            volumes,
                            labels,
                            env_vars=None,
                            command=None,
                            args=None,
                            init_command=None,
                            init_args=None,
                            init_env_vars=None,
                            ports=None,
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
                            restart_policy=None,
                            init_context_mounts=None,
                            sidecar_context_mounts=None,
                            replicas=1):
        annotations = None
        if requests_tpu(resources):
            annotations = get_tpu_annotations()
        metadata = client.V1ObjectMeta(name=resource_name,
                                       labels=labels,
                                       namespace=self.namespace,
                                       annotations=annotations)

        pod_spec = self.get_task_pod_spec(
            resource_name=resource_name,
            volume_mounts=volume_mounts,
            volumes=volumes,
            env_vars=env_vars,
            command=command,
            args=args,
            init_command=init_command,
            init_args=init_args,
            init_env_vars=init_env_vars,
            ports=ports,
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
            init_context_mounts=init_context_mounts,
            sidecar_context_mounts=sidecar_context_mounts,
            restart_policy=restart_policy)
        template_spec = client.V1PodTemplateSpec(metadata=metadata, spec=pod_spec)
        return client.AppsV1beta1DeploymentSpec(replicas=replicas, template=template_spec)

    def get_deployment(self,
                       resource_name,
                       volume_mounts,
                       volumes,
                       labels,
                       env_vars=None,
                       command=None,
                       args=None,
                       init_command=None,
                       init_args=None,
                       init_env_vars=None,
                       ports=None,
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
                       restart_policy=None,
                       init_context_mounts=None,
                       sidecar_context_mounts=None,
                       replicas=1):
        deployment_spec = self.get_deployment_spec(
            resource_name=resource_name,
            volume_mounts=volume_mounts,
            volumes=volumes,
            labels=labels,
            env_vars=env_vars,
            command=command,
            args=args,
            init_command=init_command,
            init_args=init_args,
            init_env_vars=init_env_vars,
            ports=ports,
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
            restart_policy=restart_policy,
            init_context_mounts=init_context_mounts,
            sidecar_context_mounts=sidecar_context_mounts,
            replicas=replicas,
        )
        metadata = client.V1ObjectMeta(name=resource_name, labels=labels, namespace=self.namespace)
        return client.AppsV1beta1Deployment(api_version=k8s_constants.K8S_API_VERSION_V1_BETA1,
                                            kind=k8s_constants.K8S_DEPLOYMENT_KIND,
                                            metadata=metadata,
                                            spec=deployment_spec)
