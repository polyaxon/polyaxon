import logging

from django.conf import settings

from experiments.statuses import ExperimentLifeCycle
from runner.spawners.notebook_spawner import NotebookSpawner

logger = logging.getLogger('polyaxon.schedulers.notebook')


def start_notebook(project, image):
    spawner = NotebookSpawner(
        project_name=project.unique_name,
        project_uuid=project.uuid.hex,
        k8s_config=settings.K8S_CONFIG,
        namespace=settings.K8S_NAMESPACE,
        in_cluster=True)

    spawner.start_notebook(image=image, resources=project.notebook.compiled_spec.resources)


def stop_notebook(project, update_status=False):
    spawner = NotebookSpawner(
        project_name=project.unique_name,
        project_uuid=project.uuid.hex,
        k8s_config=settings.K8S_CONFIG,
        namespace=settings.K8S_NAMESPACE,
        in_cluster=True)

    spawner.stop_notebook()
    if update_status:
        # Update experiment status to show that its stopped
        project.notebook.set_status(status=ExperimentLifeCycle.STOPPED,
                                    message='Notebook was stopped')


def get_notebook_url(project):
    spawner = NotebookSpawner(
        project_name=project.unique_name,
        project_uuid=project.uuid.hex,
        k8s_config=settings.K8S_CONFIG,
        namespace=settings.K8S_NAMESPACE,
        in_cluster=True)
    return spawner.get_notebook_url()


def get_notebook_token(project):
    spawner = NotebookSpawner(
        project_name=project.unique_name,
        project_uuid=project.uuid.hex,
        k8s_config=settings.K8S_CONFIG,
        namespace=settings.K8S_NAMESPACE,
        in_cluster=True)
    return spawner.get_notebook_token()
