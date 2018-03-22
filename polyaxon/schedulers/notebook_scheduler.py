import logging

from django.conf import settings
from spawners.notebook_spawner import NotebookSpawner
from spawners.utils.constants import ExperimentLifeCycle

logger = logging.getLogger('polyaxon.schedulers.notebook')


def start_notebook(project, image):
    spawner = NotebookSpawner(
        project_name=project.unique_name,
        project_uuid=project.uuid.hex,
        k8s_config=settings.K8S_CONFIG,
        namespace=settings.K8S_NAMESPACE,
        in_cluster=True)

    spawner.start_notebook(image=image, resources=project.notebook.compiled_spec.resources)
    project.has_notebook = True
    project.save()


def stop_notebook(project, update_status=False):
    spawner = NotebookSpawner(
        project_name=project.unique_name,
        project_uuid=project.uuid.hex,
        k8s_config=settings.K8S_CONFIG,
        namespace=settings.K8S_NAMESPACE,
        in_cluster=True)

    spawner.stop_notebook()
    project.has_notebook = False
    project.save()
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
