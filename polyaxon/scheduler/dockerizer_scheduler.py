import logging

from django.conf import settings
from kubernetes.client.rest import ApiException

from constants.jobs import JobLifeCycle
from scheduler.spawners.dockerizer_spawner import DockerizerSpawner
from scheduler.spawners.utils import get_job_definition

logger = logging.getLogger('polyaxon.scheduler.dockerizer')


def start_dockerizer(build_job):
    spawner = DockerizerSpawner(
        project_name=build_job.project.unique_name,
        project_uuid=build_job.project.uuid.hex,
        job_name=build_job.unique_name,
        job_uuid=build_job.uuid.hex,
        k8s_config=settings.K8S_CONFIG,
        namespace=settings.K8S_NAMESPACE,
        in_cluster=True)

    try:
        results = spawner.start_dockerizer(commit=build_job.commit,
                                           resources=build_job.resources,
                                           node_selectors=build_job.node_selectors)
    except ApiException as e:
        logger.warning('Could not start build job, please check your polyaxon spec %s', e)
        build_job.set_status(
            JobLifeCycle.FAILED,
            message='Could not start build job, encountered a Kubernetes ApiException.')
        return
    except Exception as e:
        logger.warning('Could not start build job, please check your polyaxon spec %s', e)
        build_job.set_status(
            JobLifeCycle.FAILED,
            message='Could not start build job encountered an {} exception.'.format(
                e.__class__.__name__
            ))
        return
    build_job.definition = get_job_definition(results)
    build_job.save()


def stop_dockerizer(build_job, update_status=False):
    spawner = DockerizerSpawner(
        project_name=build_job.project.unique_name,
        project_uuid=build_job.project.uuid.hex,
        job_name=build_job.unique_name,
        job_uuid=build_job.uuid.hex,
        k8s_config=settings.K8S_CONFIG,
        namespace=settings.K8S_NAMESPACE,
        in_cluster=True)

    spawner.stop_dockerizer()
    if update_status:
        # Update experiment status to show that its stopped
        build_job.set_status(status=JobLifeCycle.STOPPED,
                             message='BuildJob was stopped')
