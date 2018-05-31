import logging

from django.conf import settings
from kubernetes.client.rest import ApiException

from constants.jobs import JobLifeCycle
from scheduler.spawners.notebook_spawner import NotebookSpawner
from scheduler.spawners.utils import get_job_definition

logger = logging.getLogger('polyaxon.scheduler.notebook')


def start_notebook(notebook, image):
    spawner = NotebookSpawner(
        project_name=notebook.project.unique_name,
        project_uuid=notebook.project.uuid.hex,
        job_name=notebook.unique_name,
        job_uuid=notebook.uuid.hex,
        k8s_config=settings.K8S_CONFIG,
        namespace=settings.K8S_NAMESPACE,
        in_cluster=True)

    try:
        results = spawner.start_notebook(image=image,
                                         resources=notebook.resources,
                                         node_selectors=notebook.node_selectors)
    except ApiException as e:
        logger.warning('Could not start notebook, please check your polyaxon spec %s', e)
        notebook.set_status(
            JobLifeCycle.FAILED,
            message='Could not start notebook, encountered a Kubernetes ApiException.')
        return
    except Exception as e:
        logger.warning('Could not start notebook, please check your polyaxon spec %s', e)
        notebook.set_status(
            JobLifeCycle.FAILED,
            message='Could not start notebook encountered an {} exception.'.format(
                e.__class__.__name__
            ))
        return
    notebook.definition = get_job_definition(results)
    notebook.save()


def stop_notebook(notebook, update_status=False):
    spawner = NotebookSpawner(
        project_name=notebook.project.unique_name,
        project_uuid=notebook.project.uuid.hex,
        job_name=notebook.unique_name,
        job_uuid=notebook.uuid.hex,
        k8s_config=settings.K8S_CONFIG,
        namespace=settings.K8S_NAMESPACE,
        in_cluster=True)

    spawner.stop_notebook()
    if update_status:
        # Update experiment status to show that its stopped
        notebook.set_status(status=JobLifeCycle.STOPPED,
                            message='Notebook was stopped')


def get_notebook_url(notebook):
    spawner = NotebookSpawner(
        project_name=notebook.project.unique_name,
        project_uuid=notebook.project.uuid.hex,
        job_name=notebook.unique_name,
        job_uuid=notebook.uuid.hex,
        k8s_config=settings.K8S_CONFIG,
        namespace=settings.K8S_NAMESPACE,
        in_cluster=True)
    return spawner.get_notebook_url()


def get_notebook_token(notebook):
    spawner = NotebookSpawner(
        project_name=notebook.project.unique_name,
        project_uuid=notebook.project.uuid.hex,
        job_name=notebook.unique_name,
        job_uuid=notebook.uuid.hex,
        k8s_config=settings.K8S_CONFIG,
        namespace=settings.K8S_NAMESPACE,
        in_cluster=True)
    return spawner.get_notebook_token()
