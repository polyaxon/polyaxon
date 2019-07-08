import logging
import traceback

from kubernetes.client.rest import ApiException

import conf

from libs.unique_urls import get_notebook_reconcile_url
from lifecycles.jobs import JobLifeCycle
from options.registry.k8s import K8S_CONFIG, K8S_NAMESPACE
from options.registry.notebooks import NOTEBOOKS_MOUNT_CODE
from options.registry.restarts import MAX_RESTARTS_NOTEBOOKS
from registry.exceptions import ContainerRegistryError
from registry.image_info import get_image_info
from registry.registry_context import get_registry_context
from scheduler.spawners.notebook_spawner import NotebookSpawner
from scheduler.spawners.templates.restart_policy import get_max_restart
from scheduler.spawners.utils import get_job_definition
from stores.exceptions import StoreNotFoundError

_logger = logging.getLogger('polyaxon.scheduler.notebook')


def start_notebook(notebook):
    # Update job status to show that its started
    notebook.set_status(JobLifeCycle.SCHEDULED)

    try:
        registry_spec = get_registry_context(build_backend=None)
    except ContainerRegistryError:
        notebook.set_status(
            JobLifeCycle.FAILED,
            message='Could not start the notebook, please check your registry configuration.')
        return

    try:
        image_name, image_tag = get_image_info(build_job=notebook.build_job,
                                               registry_host=registry_spec.host)
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
        k8s_config=conf.get(K8S_CONFIG),
        namespace=conf.get(K8S_NAMESPACE),
        job_docker_image=job_docker_image,
        in_cluster=True)

    error = {}
    try:
        mount_code_in_notebooks = conf.get(NOTEBOOKS_MOUNT_CODE)
        results = spawner.start_notebook(
            persistence_outputs=notebook.persistence_outputs,
            persistence_data=notebook.persistence_data,
            outputs_refs_jobs=notebook.outputs_refs_jobs,
            outputs_refs_experiments=notebook.outputs_refs_experiments,
            resources=notebook.resources,
            labels=notebook.labels,
            annotations=notebook.annotations,
            secret_refs=notebook.secret_refs,
            config_map_refs=notebook.config_map_refs,
            node_selector=notebook.node_selector,
            affinity=notebook.affinity,
            tolerations=notebook.tolerations,
            backend=notebook.backend,
            max_restarts=get_max_restart(notebook.max_restarts, conf.get(MAX_RESTARTS_NOTEBOOKS)),
            reconcile_url=get_notebook_reconcile_url(notebook.unique_name),
            mount_code_in_notebooks=mount_code_in_notebooks)
        notebook.definition = get_job_definition(results)
        notebook.save(update_fields=['definition'])
        return
    except ApiException:
        _logger.error('Could not start notebook, please check your polyaxon spec.',
                      exc_info=True)
        error = {
            'raised': True,
            'traceback': traceback.format_exc(),
            'message': 'Could not start the job, encountered a Kubernetes ApiException.',
        }
    except StoreNotFoundError as e:
        _logger.error('Could not start the notebook, please check your volume definitions',
                      exc_info=True)
        error = {
            'raised': True,
            'traceback': traceback.format_exc(),
            'message': 'Could not start the job, encountered a volume definition problem. %s' % e,
        }
    except Exception as e:
        _logger.error('Could not start notebook, please check your polyaxon spec.',
                      exc_info=True)
        error = {
            'raised': True,
            'traceback': traceback.format_exc(),
            'message': 'Could not start notebook encountered an {} exception.'.format(
                e.__class__.__name__)
        }
    finally:
        if error.get('raised'):
            notebook.set_status(
                JobLifeCycle.FAILED,
                message=error.get('message'),
                traceback=error.get('traceback'))


def stop_notebook(project_name,
                  project_uuid,
                  notebook_job_name,
                  notebook_job_uuid):
    spawner = NotebookSpawner(
        project_name=project_name,
        project_uuid=project_uuid,
        job_name=notebook_job_name,
        job_uuid=notebook_job_uuid,
        k8s_config=conf.get(K8S_CONFIG),
        namespace=conf.get(K8S_NAMESPACE),
        in_cluster=True)

    return spawner.stop_notebook()


def get_notebook_url(notebook):
    spawner = NotebookSpawner(
        project_name=notebook.project.unique_name,
        project_uuid=notebook.project.uuid.hex,
        job_name=notebook.unique_name,
        job_uuid=notebook.uuid.hex,
        k8s_config=conf.get(K8S_CONFIG),
        namespace=conf.get(K8S_NAMESPACE),
        in_cluster=True)
    return spawner.get_notebook_url()


def get_notebook_token(notebook):
    spawner = NotebookSpawner(
        project_name=notebook.project.unique_name,
        project_uuid=notebook.project.uuid.hex,
        job_name=notebook.unique_name,
        job_uuid=notebook.uuid.hex,
        k8s_config=conf.get(K8S_CONFIG),
        namespace=conf.get(K8S_NAMESPACE),
        in_cluster=True)
    return spawner.get_notebook_token()
