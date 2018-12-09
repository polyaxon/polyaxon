from django.conf import settings

from constants.k8s_jobs import JOB_NAME_FORMAT, DOCKERIZER_JOB_NAME
from polyaxon.config_manager import config
from polyaxon_k8s.exceptions import PolyaxonK8SError
from scheduler.spawners.project_job_spawner import ProjectJobSpawner
from scheduler.spawners.templates.env_vars import get_env_var, get_from_secret, get_service_env_vars
from scheduler.spawners.templates.pod_environment import (
    get_affinity,
    get_node_selector,
    get_tolerations
)
from scheduler.spawners.templates.project_jobs import pods
from scheduler.spawners.templates.volumes import get_docker_volumes


class DockerizerSpawner(ProjectJobSpawner):
    def get_env_vars(self):
        env_vars = get_service_env_vars(namespace=self.namespace)
        for k, v in config.get_requested_params(to_str=True).items():
            env_vars.append(get_env_var(name=k, value=v))

        # Add private registries secrets keys
        for key in config.params_startswith(settings.PRIVATE_REGISTRIES_PREFIX):
            env_vars.append(get_from_secret(key, key))

        # Add repos access token secret key
        if settings.REPOS_ACCESS_TOKEN:
            env_vars.append(get_from_secret(settings.REPOS_ACCESS_TOKEN_KEY,
                                            settings.REPOS_ACCESS_TOKEN_KEY))

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
        pod = pods.get_pod(
            namespace=self.namespace,
            app=settings.APP_LABELS_DOCKERIZER,
            name=DOCKERIZER_JOB_NAME,
            project_name=self.project_name,
            project_uuid=self.project_uuid,
            job_name=self.job_name,
            job_uuid=self.job_uuid,
            volume_mounts=volume_mounts,
            volumes=volumes,
            image=settings.JOB_DOCKERIZER_IMAGE,
            image_pull_policy=settings.JOB_DOCKERIZER_IMAGE_PULL_POLICY,
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
            type=settings.TYPE_LABELS_RUNNER,
            restart_policy='Never')
        pod_name = JOB_NAME_FORMAT.format(job_uuid=self.job_uuid, name=DOCKERIZER_JOB_NAME)

        pod_resp, _ = self.create_or_update_pod(name=pod_name, data=pod)
        return pod_resp.to_dict()

    def stop_dockerizer(self):
        pod_name = JOB_NAME_FORMAT.format(job_uuid=self.job_uuid, name=DOCKERIZER_JOB_NAME)
        try:
            self.delete_pod(name=pod_name, reraise=True)
            return True
        except PolyaxonK8SError:
            return False
