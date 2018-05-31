import logging

from django.conf import settings
from kubernetes.client.rest import ApiException

from constants.jobs import JobLifeCycle
from scheduler.spawners.notebook_spawner import NotebookSpawner
from scheduler.spawners.utils import get_job_definition

logger = logging.getLogger('polyaxon.scheduler.notebook')


def start_notebook(project, image):
    spawner = NotebookSpawner(
        project_name=project.unique_name,
        project_uuid=project.uuid.hex,
        k8s_config=settings.K8S_CONFIG,
        namespace=settings.K8S_NAMESPACE,
        in_cluster=True)

    try:
        results = spawner.start_notebook(image=image,
                                         resources=project.notebook.resources,
                                         node_selectors=project.notebook.node_selectors)
    except ApiException as e:
        logger.warning('Could not start notebook, please check your polyaxon spec %s', e)
        project.notebook.set_status(
            JobLifeCycle.FAILED,
            message='Could not start notebook, encountered a Kubernetes ApiException.')
        return
    except Exception as e:
        logger.warning('Could not start notebook, please check your polyaxon spec %s', e)
        project.notebook.set_status(
            JobLifeCycle.FAILED,
            message='Could not start notebook encountered an {} exception.'.format(
                e.__class__.__name__
            ))
        return
    project.notebook.definition = get_job_definition(results)
    project.notebook.save()


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
        project.notebook.set_status(status=JobLifeCycle.STOPPED,
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
