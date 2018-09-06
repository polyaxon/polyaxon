from django.conf import settings

from polyaxon.config_manager import config
from scheduler.spawners.project_job_spawner import ProjectJobSpawner
from scheduler.spawners.templates import constants
from scheduler.spawners.templates.env_vars import get_env_var, get_from_secret, get_service_env_vars
from scheduler.spawners.templates.pod_environment import (
    get_affinity,
    get_node_selector,
    get_tolerations
)
from scheduler.spawners.templates.project_jobs import pods
from scheduler.spawners.templates.volumes import get_docker_volumes


class DockerizerSpawner(ProjectJobSpawner):
    DOCKERIZER_JOB_NAME = 'build'

    def get_env_vars(self):
        env_vars = get_service_env_vars(namespace=self.namespace)
        for k, v in config.get_requested_params(to_str=True).items():
            env_vars.append(get_env_var(name=k, value=v))

        # Add private registries secrets keys
        for key in config.params_startswith(settings.PRIVATE_REGISTRIES_PREFIX):
            env_vars.append(get_from_secret(key, key))

        return env_vars

    def start_dockerizer(self,
                         resources=None,
                         node_selector=None,
                         affinity=None,
                         tolerations=None):
        volumes, volume_mounts = get_docker_volumes()

        node_selector = get_node_selector(
            node_selector=node_selector,
            default_node_selector=settings.NODE_SELECTOR_BUILDS)
        affinity = get_affinity(
            affinity=affinity,
            default_affinity=settings.AFFINITY_BUILDS)
        tolerations = get_tolerations(
            tolerations=tolerations,
            default_tolerations=settings.TOLERATIONS_BUILDS)
        deployment = pods.get_pod(
            namespace=self.namespace,
            app=settings.APP_LABELS_DOCKERIZER,
            name=self.DOCKERIZER_JOB_NAME,
            project_name=self.project_name,
            project_uuid=self.project_uuid,
            job_name=self.job_name,
            job_uuid=self.job_uuid,
            volume_mounts=volume_mounts,
            volumes=volumes,
            image=settings.JOB_DOCKERIZER_IMAGE,
            command=None,
            args=[self.job_uuid],
            ports=[],
            env_vars=self.get_env_vars(),
            container_name=settings.CONTAINER_NAME_DOCKERIZER_JOB,
            resources=resources,
            node_selector=node_selector,
            affinity=affinity,
            tolerations=tolerations,
            role=settings.ROLE_LABELS_WORKER,
            type=settings.TYPE_LABELS_EXPERIMENT,
            restart_policy='Never')
        pod_name = constants.JOB_NAME.format(
            job_uuid=self.job_uuid, name=self.DOCKERIZER_JOB_NAME)

        pod_resp, _ = self.create_or_update_pod(name=pod_name, data=deployment)
        return pod_resp.to_dict()

    def stop_dockerizer(self):
        pod_name = constants.JOB_NAME.format(job_uuid=self.job_uuid,
                                             name=self.DOCKERIZER_JOB_NAME)
        self.delete_pod(name=pod_name)
