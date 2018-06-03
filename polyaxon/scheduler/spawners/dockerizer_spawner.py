import logging

from django.conf import settings

from polyaxon.utils import config

from libs.api import API_URL
from scheduler.spawners.project_job_spawner import ProjectJobSpawner
from scheduler.spawners.templates import constants
from scheduler.spawners.templates.env_vars import get_env_var, get_from_app_secret
from scheduler.spawners.templates.project_jobs import pods
from scheduler.spawners.templates.services.default_env_vars import get_service_env_vars

logger = logging.getLogger('polyaxon.spawners.dockerizer')


class DockerizerSpawner(ProjectJobSpawner):
    DOCKERIZER_JOB_NAME = 'build'

    def get_env_vars(self):
        env_vars = [get_env_var(name='POLYAXON_K8S_NAMESPACE', value=self.namespace)]
        env_vars += get_service_env_vars()
        for k, v in config.get_requested_params(to_str=True).items():
            env_vars.append(get_env_var(name=k, value=v))

        return env_vars

    def start_dockerizer(self, commit, resources=None, node_selectors=None):
        deployment = pods.get_pod(
            namespace=self.namespace,
            app=settings.APP_LABELS_DOCKERIZER,
            name=self.DOCKERIZER_JOB_NAME.format(commit),
            project_name=self.project_name,
            project_uuid=self.project_uuid,
            job_name=self.job_name,
            job_uuid=self.job_uuid,
            volume_mounts=[],
            volumes=[],
            image=settings.JOB_DOCKERIZER_IMAGE,
            command=None,
            args=["--build_job_uuid={}".format(self.job_uuid)],
            ports=[],
            env_vars=self.get_env_vars(),
            container_name=settings.CONTAINER_NAME_DOCKERIZER_JOB,
            resources=resources,
            node_selector=node_selectors,
            role=settings.ROLE_LABELS_WORKER,
            type=settings.TYPE_LABELS_EXPERIMENT,
            restart_policy='Never')
        pod_name = constants.DEPLOYMENT_NAME.format(
            job_uuid=self.job_uuid, name=self.DOCKERIZER_JOB_NAME)

        return self.create_or_update_pod(name=pod_name, data=deployment).to_dict()

    def stop_dockerizer(self):
        pod_name = constants.DEPLOYMENT_NAME.format(job_uuid=self.job_uuid,
                                                    name=self.DOCKERIZER_JOB_NAME)
        self.delete_pod(name=pod_name)
