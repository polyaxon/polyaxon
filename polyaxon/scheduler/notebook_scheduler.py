import logging

from kubernetes.client.rest import ApiException

from django.conf import settings

from constants.jobs import JobLifeCycle
from docker_images.image_info import get_image_info
from libs.paths.exceptions import VolumeNotFoundError
from scheduler.spawners.notebook_spawner import NotebookSpawner
from scheduler.spawners.utils import get_job_definition

_logger = logging.getLogger('polyaxon.scheduler.notebook')


def start_notebook(notebook):
    # Update job status to show that its started
    notebook.set_status(JobLifeCycle.SCHEDULED)

    try:
        image_name, image_tag = get_image_info(build_job=notebook.build_job)
    except (ValueError, AttributeError):
        _logger.error('Could not start the notebook.', exc_info=True)
        notebook.set_status(JobLifeCycle.FAILED,
                            message='Image info was not found.')
        return
    job_docker_image = '{}:{}'.format(image_name, image_tag)
    _logger.info('Start notebook with built image `%s`', job_docker_image)

    spawner = NotebookSpawner(
        project_name=notebook.project.unique_name,
        project_uuid=notebook.project.uuid.hex,
        job_name=notebook.unique_name,
        job_uuid=notebook.uuid.hex,
        k8s_config=settings.K8S_CONFIG,
        namespace=settings.K8S_NAMESPACE,
        in_cluster=True)

    try:
        allow_commits = False
        if settings.REPOS_CLAIM_NAME or notebook.node_selector:
            allow_commits = True
        results = spawner.start_notebook(image=job_docker_image,
                                         persistence_outputs=notebook.persistence_outputs,
                                         persistence_data=notebook.persistence_data,
                                         outputs_refs_jobs=notebook.outputs_refs_jobs,
                                         outputs_refs_experiments=notebook.outputs_refs_experiments,
                                         resources=notebook.resources,
                                         node_selector=notebook.node_selector,
                                         affinity=notebook.affinity,
                                         tolerations=notebook.tolerations,
                                         allow_commits=allow_commits)
    except ApiException:
        _logger.error('Could not start notebook, please check your polyaxon spec.',
                      exc_info=True)
        notebook.set_status(
            JobLifeCycle.FAILED,
            message='Could not start notebook, encountered a Kubernetes ApiException.')
        return
    except VolumeNotFoundError as e:
        _logger.error('Could not start the notebook, please check your volume definitions',
                      exc_info=True)
        notebook.set_status(
            JobLifeCycle.FAILED,
            message='Could not start the notebook, '
                    'encountered a volume definition problem. %s' % e)
        return False
    except Exception as e:
        _logger.error('Could not start notebook, please check your polyaxon spec.',
                      exc_info=True)
        notebook.set_status(
            JobLifeCycle.FAILED,
            message='Could not start notebook encountered an {} exception.'.format(
                e.__class__.__name__
            ))
        return
    notebook.definition = get_job_definition(results)
    notebook.save()


def stop_notebook(project_name,
                  project_uuid,
                  notebook_job_name,
                  notebook_job_uuid):
    spawner = NotebookSpawner(
        project_name=project_name,
        project_uuid=project_uuid,
        job_name=notebook_job_name,
        job_uuid=notebook_job_uuid,
        k8s_config=settings.K8S_CONFIG,
        namespace=settings.K8S_NAMESPACE,
        in_cluster=True)

    spawner.stop_notebook()


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
