import logging

from django.conf import settings

from scheduler.spawners.project_spawner import ProjectSpawner
from scheduler.spawners.templates import constants, deployments

logger = logging.getLogger('polyaxon.spawners.tensorboard')


class DockerizerSpawner(ProjectSpawner):
    DOCKERIZER_JOB_NAME = 'build-{}'

    def build_notebook(self, project_uuid, commit, resources=None, node_selectors=None):
        command_args = ["notebook", "{}".format(project_uuid)]
        self.start_dockerizer(commit=commit,
                              command_args=command_args,
                              resources=resources,
                              node_selectors=node_selectors)

    def build_experiment(self, experiment_uuid, commit, resources=None, node_selectors=None):
        command_args = ["experiment", "{}".format(experiment_uuid)]
        self.start_dockerizer(commit=commit,
                              command_args=command_args,
                              resources=resources,
                              node_selectors=node_selectors)

    def start_dockerizer(self, commit, command_args, resources=None, node_selectors=None):
        deployment = deployments.get_deployment(
            namespace=self.namespace,
            app=settings.APP_LABELS_TENSORBOARD,
            name=self.DOCKERIZER_JOB_NAME.format(commit),
            project_name=self.project_name,
            project_uuid=self.project_uuid,
            volume_mounts=[],
            volumes=[],
            image=settings.DOCKERIZER_IMAGE,
            command=None,
            args=command_args,
            ports=[],
            container_name=settings.CONTAINER_NAME_DOCKERIZER_JOB,
            resources=resources,
            node_selector=node_selectors,
            role=settings.ROLE_LABELS_DOCKERIZER,
            type=settings.TYPE_LABELS_EXPERIMENT)
        deployment_name = constants.DEPLOYMENT_NAME.format(
            project_uuid=self.project_uuid, name=self.DOCKERIZER_JOB_NAME)

        self.create_or_update_deployment(name=deployment_name, data=deployment)

    def stop_dockerizer(self, commit):
        name = self.DOCKERIZER_JOB_NAME.format(commit)
        deployment_name = constants.DEPLOYMENT_NAME.format(project_uuid=self.project_uuid,
                                                           name=name)
        self.delete_deployment(name=deployment_name)
