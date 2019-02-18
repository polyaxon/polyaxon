from hestia.auth import AuthenticationTypes
from hestia.internal_services import InternalServices

from constants.k8s_jobs import JOB_NAME
from libs.unique_urls import get_job_health_url
from polyaxon_k8s.exceptions import PolyaxonK8SError
from polyaxon_k8s.manager import K8SManager
from scheduler.spawners.templates.env_vars import (
    get_internal_env_vars,
    validate_configmap_refs,
    validate_secret_refs
)
from scheduler.spawners.templates.jobs import manager
from scheduler.spawners.templates.pod_cmd import get_pod_command_args
from scheduler.spawners.templates.volumes import (
    get_auth_context_volumes,
    get_pod_refs_outputs_volumes,
    get_pod_volumes,
    get_shm_volumes
)


class JobSpawner(K8SManager):
    def __init__(self,
                 project_name,
                 project_uuid,
                 job_name,
                 job_uuid,
                 spec,
                 k8s_config=None,
                 namespace='default',
                 in_cluster=False,
                 job_container_name=None,
                 job_docker_image=None,
                 sidecar_container_name=None,
                 sidecar_docker_image=None,
                 role_label=None,
                 type_label=None,
                 use_sidecar=False,
                 sidecar_config=None):
        self.spec = spec
        self.project_name = project_name
        self.project_uuid = project_uuid
        self.job_name = job_name
        self.job_uuid = job_uuid
        self.resource_manager = manager.ResourceManager(
            namespace=namespace,
            name=JOB_NAME,
            project_name=project_name,
            project_uuid=project_uuid,
            job_name=job_name,
            job_uuid=job_uuid,
            job_docker_image=job_docker_image,
            job_container_name=job_container_name,
            sidecar_container_name=sidecar_container_name,
            sidecar_docker_image=sidecar_docker_image,
            role_label=role_label,
            type_label=type_label,
            use_sidecar=use_sidecar,
            sidecar_config=sidecar_config,
            health_check_url=get_job_health_url(job_name),
            log_level=self.spec.log_level if self.spec else None)

        super().__init__(k8s_config=k8s_config,
                         namespace=namespace,
                         in_cluster=in_cluster)

    def get_pod_command_args(self):
        return get_pod_command_args(run_config=self.spec.run)

    def get_init_env_vars(self):
        env_vars = get_internal_env_vars(service_internal_header=InternalServices.INITIALIZER,
                                         namespace=self.namespace,
                                         authentication_type=AuthenticationTypes.INTERNAL_TOKEN,
                                         include_internal_token=True)
        return env_vars

    def start_job(self,
                  persistence_outputs=None,
                  persistence_data=None,
                  outputs_refs_jobs=None,
                  outputs_refs_experiments=None,
                  resources=None,
                  node_selector=None,
                  affinity=None,
                  tolerations=None):
        # Set and validate volumes
        volumes, volume_mounts = get_pod_volumes(persistence_outputs=persistence_outputs,
                                                 persistence_data=persistence_data)
        refs_volumes, refs_volume_mounts = get_pod_refs_outputs_volumes(
            outputs_refs=outputs_refs_jobs,
            persistence_outputs=persistence_outputs)
        volumes += refs_volumes
        volume_mounts += refs_volume_mounts
        refs_volumes, refs_volume_mounts = get_pod_refs_outputs_volumes(
            outputs_refs=outputs_refs_experiments,
            persistence_outputs=persistence_outputs)
        volumes += refs_volumes
        volume_mounts += refs_volume_mounts
        shm_volumes, shm_volume_mounts = get_shm_volumes()
        volumes += shm_volumes
        volume_mounts += shm_volume_mounts

        context_volumes, context_mounts = get_auth_context_volumes()
        volumes += context_volumes
        volume_mounts += context_mounts

        # Validate secret and configmap refs
        secret_refs = validate_secret_refs(self.spec.secret_refs)
        configmap_refs = validate_configmap_refs(self.spec.configmap_refs)

        command, args = self.get_pod_command_args()
        resource_name = self.resource_manager.get_resource_name()
        pod = self.resource_manager.get_pod(
            resource_name=resource_name,
            volume_mounts=volume_mounts,
            volumes=volumes,
            labels=self.resource_manager.labels,
            env_vars=None,
            command=command,
            args=args,
            init_env_vars=self.get_init_env_vars(),
            persistence_outputs=persistence_outputs,
            persistence_data=persistence_data,
            outputs_refs_jobs=outputs_refs_jobs,
            outputs_refs_experiments=outputs_refs_experiments,
            secret_refs=secret_refs,
            configmap_refs=configmap_refs,
            resources=resources,
            ephemeral_token=None,
            node_selector=node_selector,
            affinity=affinity,
            tolerations=tolerations,
            init_context_mounts=context_mounts,
            restart_policy='Never')
        pod_resp, _ = self.create_or_update_pod(name=resource_name, data=pod)

        return pod_resp.to_dict()

    def stop_job(self):
        try:
            self.delete_pod(name=self.resource_manager.get_resource_name(), reraise=True)
            return True
        except PolyaxonK8SError:
            return False
