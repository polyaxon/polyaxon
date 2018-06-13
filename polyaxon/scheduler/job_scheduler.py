import logging

from kubernetes.client.rest import ApiException

from django.conf import settings

from constants.jobs import JobLifeCycle
from docker_images.image_info import get_image_info
from polyaxon.utils import config
from scheduler.spawners.job_spawner import JobSpawner
from scheduler.spawners.utils import get_job_definition

_logger = logging.getLogger('polyaxon.scheduler.notebook')


def start_job(job):
    # Update job status to show that its started
    job.set_status(JobLifeCycle.SCHEDULED)

    try:
        image_name, image_tag = get_image_info(build_job=job.build_job)
    except ValueError as e:
        _logger.warning('Could not start the job, %s', e)
        job.set_status(JobLifeCycle.FAILED, message='External git repo was note found.')
        return
    job_docker_image = '{}:{}'.format(image_name, image_tag)
    _logger.info('Start job with built image `%s`', job_docker_image)

    spawner = JobSpawner(
        project_name=job.project.unique_name,
        project_uuid=job.project.uuid.hex,
        job_name=job.unique_name,
        job_uuid=job.uuid.hex,
        spec=job.specification,
        k8s_config=settings.K8S_CONFIG,
        namespace=settings.K8S_NAMESPACE,
        job_docker_image=job_docker_image,
        in_cluster=True,
        use_sidecar=True,
        sidecar_config=config.get_requested_params(to_str=True))

    try:
        results = spawner.start_job(resources=job.resources,
                                    node_selectors=job.node_selectors)
    except ApiException as e:
        _logger.warning('Could not start job, please check your polyaxon spec %s', e)
        job.set_status(
            JobLifeCycle.FAILED,
            message='Could not start job, encountered a Kubernetes ApiException.')
        return
    except Exception as e:
        _logger.warning('Could not start job, please check your polyaxon spec %s', e)
        job.set_status(
            JobLifeCycle.FAILED,
            message='Could not start job encountered an {} exception.'.format(
                e.__class__.__name__
            ))
        return
    job.definition = get_job_definition(results)
    job.save()


def stop_job(project_name, project_uuid, job_name, job_uuid, specification):
    spawner = JobSpawner(
        project_name=project_name,
        project_uuid=project_uuid,
        job_name=job_name,
        job_uuid=job_uuid,
        spec=specification,
        k8s_config=settings.K8S_CONFIG,
        namespace=settings.K8S_NAMESPACE,
        in_cluster=True)

    spawner.stop_job()
