import logging

from kubernetes.client.rest import ApiException

from django.conf import settings

from constants.jobs import JobLifeCycle
from scheduler.spawners.job_spawner import JobSpawner
from scheduler.spawners.utils import get_job_definition

logger = logging.getLogger('polyaxon.scheduler.notebook')


def start_job(job):
    spawner = JobSpawner(
        project_name=job.project.unique_name,
        project_uuid=job.project.uuid.hex,
        job_name=job.unique_name,
        job_uuid=job.uuid.hex,
        spec=job.specification,
        k8s_config=settings.K8S_CONFIG,
        namespace=settings.K8S_NAMESPACE,
        in_cluster=True)

    try:
        results = spawner.start_job(resources=job.resources,
                                    node_selectors=job.node_selectors)
    except ApiException as e:
        logger.warning('Could not start job, please check your polyaxon spec %s', e)
        job.set_status(
            JobLifeCycle.FAILED,
            message='Could not start job, encountered a Kubernetes ApiException.')
        return
    except Exception as e:
        logger.warning('Could not start job, please check your polyaxon spec %s', e)
        job.set_status(
            JobLifeCycle.FAILED,
            message='Could not start job encountered an {} exception.'.format(
                e.__class__.__name__
            ))
        return
    job.definition = get_job_definition(results)
    job.save()


def stop_job(job, update_status=False):
    spawner = JobSpawner(
        project_name=job.project.unique_name,
        project_uuid=job.project.uuid.hex,
        job_name=job.unique_name,
        job_uuid=job.uuid.hex,
        spec=job.specification,
        k8s_config=settings.K8S_CONFIG,
        namespace=settings.K8S_NAMESPACE,
        in_cluster=True)

    spawner.stop_job()
    if update_status:
        # Update experiment status to show that its stopped
        job.set_status(status=JobLifeCycle.STOPPED,
                       message='Job was stopped')
