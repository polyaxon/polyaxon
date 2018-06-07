from django.conf import settings

from polyaxon.utils import config
from scheduler.spawners.project_job_spawner import ProjectJobSpawner
from scheduler.spawners.templates import constants
from scheduler.spawners.templates.env_vars import get_env_var
from scheduler.spawners.templates.internal_services_env_vars import get_service_env_vars
from scheduler.spawners.templates.project_jobs import pods
from scheduler.spawners.templates.volumes import get_docker_volumes


class DockerizerSpawner(ProjectJobSpawner):
    DOCKERIZER_JOB_NAME = 'build'

    def get_env_vars(self):
        env_vars = [get_env_var(name='POLYAXON_K8S_NAMESPACE', value=self.namespace)]
        env_vars += get_service_env_vars()
        for k, v in config.get_requested_params(to_str=True).items():
            env_vars.append(get_env_var(name=k, value=v))

        return env_vars

    def start_dockerizer(self, resources=None, node_selectors=None):
        volumes, volume_mounts = get_docker_volumes()
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
            node_selector=node_selectors,
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
