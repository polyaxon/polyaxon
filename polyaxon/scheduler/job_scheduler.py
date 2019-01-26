import logging
import traceback

from kubernetes.client.rest import ApiException

import conf

from constants.jobs import JobLifeCycle
from docker_images.image_info import get_image_info
from scheduler.spawners.job_spawner import JobSpawner
from scheduler.spawners.utils import get_job_definition
from stores.exceptions import VolumeNotFoundError

_logger = logging.getLogger('polyaxon.scheduler.notebook')


def start_job(job):
    # Update job status to show that its started
    job.set_status(JobLifeCycle.SCHEDULED)

    try:
        image_name, image_tag = get_image_info(build_job=job.build_job)
    except (ValueError, AttributeError):
        _logger.error('Could not start the job.', exc_info=True)
        job.set_status(JobLifeCycle.FAILED,
                       message='Image info was not found.')
        return
    job_docker_image = '{}:{}'.format(image_name, image_tag)
    _logger.info('Start job with built image `%s`', job_docker_image)

    spawner = JobSpawner(
        project_name=job.project.unique_name,
        project_uuid=job.project.uuid.hex,
        job_name=job.unique_name,
        job_uuid=job.uuid.hex,
        spec=job.specification,
        k8s_config=conf.get('K8S_CONFIG'),
        namespace=conf.get('K8S_NAMESPACE'),
        job_docker_image=job_docker_image,
        in_cluster=True,
        use_sidecar=True)

    error = {}
    try:
        results = spawner.start_job(persistence_data=job.persistence_data,
                                    persistence_outputs=job.persistence_outputs,
                                    outputs_refs_jobs=job.outputs_refs_jobs,
                                    outputs_refs_experiments=job.outputs_refs_experiments,
                                    resources=job.resources,
                                    node_selector=job.node_selector,
                                    affinity=job.affinity,
                                    tolerations=job.tolerations)
        job.definition = get_job_definition(results)
        job.save(update_fields=['definition'])
        return
    except ApiException:
        _logger.error('Could not start job, please check your polyaxon spec.',
                      exc_info=True)
        error = {
            'raised': True,
            'traceback': traceback.format_exc(),
            'message': 'Could not start the job, encountered a Kubernetes ApiException.',
        }
    except VolumeNotFoundError as e:
        _logger.error('Could not start the job, please check your volume definitions.',
                      exc_info=True)
        error = {
            'raised': True,
            'traceback': traceback.format_exc(),
            'message': 'Could not start the job, encountered a volume definition problem. %s' % e,
        }
    except Exception as e:
        _logger.error('Could not start job, please check your polyaxon spec.',
                      exc_info=True)
        error = {
            'raised': True,
            'traceback': traceback.format_exc(),
            'message': 'Could not start job encountered an {} exception.'.format(
                e.__class__.__name__)
        }
    finally:
        if error.get('raised'):
            job.set_status(
                JobLifeCycle.FAILED,
                message=error.get('message'),
                traceback=error.get('traceback'))


def stop_job(project_name, project_uuid, job_name, job_uuid):
    spawner = JobSpawner(
        project_name=project_name,
        project_uuid=project_uuid,
        job_name=job_name,
        job_uuid=job_uuid,
        k8s_config=conf.get('K8S_CONFIG'),
        namespace=conf.get('K8S_NAMESPACE'),
        spec=None,
        in_cluster=True)

    return spawner.stop_job()
