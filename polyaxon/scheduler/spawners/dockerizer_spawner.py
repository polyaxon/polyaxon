from django.conf import settings

from constants.k8s_jobs import DOCKERIZER_JOB_NAME
from libs.unique_urls import get_build_health_url
from polyaxon.config_manager import config
from polyaxon_k8s.exceptions import PolyaxonK8SError
from polyaxon_k8s.manager import K8SManager
from scheduler.spawners.templates.dockerizers import manager
from scheduler.spawners.templates.env_vars import get_env_var, get_from_secret, get_service_env_vars
from scheduler.spawners.templates.volumes import get_build_context_volumes, get_docker_volumes


class DockerizerSpawner(K8SManager):
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
            name=DOCKERIZER_JOB_NAME,
            project_name=self.project_name,
            project_uuid=self.project_uuid,
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
            health_check_url=get_build_health_url(job_name),
            log_level=self.spec.log_level if self.spec else None)

        super().__init__(k8s_config=k8s_config,
                         namespace=namespace,
                         in_cluster=in_cluster)

    def get_env_vars(self):
        env_vars = get_service_env_vars(namespace=self.namespace)
        for k, v in config.get_requested_data(to_str=True).items():
            env_vars.append(get_env_var(name=k, value=v))

        # Add private registries secrets keys
        for key in config.keys_startswith(settings.PRIVATE_REGISTRIES_PREFIX):
            env_vars.append(get_from_secret(key, key))

        # Add repos access token secret key
        if settings.REPOS_ACCESS_TOKEN:
            env_vars.append(get_from_secret(settings.REPOS_ACCESS_TOKEN_KEY,
                                            settings.REPOS_ACCESS_TOKEN_KEY))

        return env_vars

    def get_pod_command_args(self):
        return ["python3", "polyaxon/manage.py", "build"], [self.job_uuid]

    def get_init_command_args(self):
        return ["python3", "polyaxon/manage.py", "init"], [self.job_uuid]

    def start_dockerizer(self,
                         resources=None,
                         node_selector=None,
                         affinity=None,
                         tolerations=None):
        volumes, volume_mounts = get_docker_volumes()
        context_volumes, context_mounts = get_build_context_volumes()
        volumes += context_volumes
        volume_mounts += context_mounts
        env_vars = self.get_env_vars()

        resource_name = self.resource_manager.get_resource_name()
        command, args = self.get_pod_command_args()
        init_command, init_args = self.get_init_command_args()
        pod = self.resource_manager.get_pod(
            resource_name=resource_name,
            volume_mounts=volume_mounts,
            volumes=volumes,
            labels=self.resource_manager.labels,
            env_vars=env_vars,
            command=command,
            args=args,
            init_command=init_command,
            init_args=init_args,
            persistence_outputs=None,
            persistence_data=None,
            outputs_refs_jobs=None,
            outputs_refs_experiments=None,
            secret_refs=None,
            configmap_refs=None,
            resources=resources,
            ephemeral_token=None,
            node_selector=node_selector,
            affinity=affinity,
            tolerations=tolerations,
            context_mounts=context_mounts,
            restart_policy='Never')

        pod_resp, _ = self.create_or_update_pod(name=resource_name, data=pod)
        return pod_resp.to_dict()

    def stop_dockerizer(self):
        try:
            self.delete_pod(name=self.resource_manager.get_resource_name(), reraise=True)
            return True
        except PolyaxonK8SError:
            return False
