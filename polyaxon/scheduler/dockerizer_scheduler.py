import logging
import traceback

from kubernetes.client.rest import ApiException

from django.conf import settings

import auditor

from constants.jobs import JobLifeCycle
from db.models.build_jobs import BuildJob
from docker_images.image_info import get_tagged_image
from event_manager.events.build_job import BUILD_JOB_STARTED, BUILD_JOB_STARTED_TRIGGERED
from stores.exceptions import VolumeNotFoundError
from scheduler.spawners.dockerizer_spawner import DockerizerSpawner
from scheduler.spawners.utils import get_job_definition

_logger = logging.getLogger('polyaxon.scheduler.dockerizer')


def check_image(build_job):
    from docker import APIClient

    docker = APIClient(version='auto')
    return docker.images(get_tagged_image(build_job))


def create_build_job(user, project, config, code_reference, configmap_refs=None, secret_refs=None):
    """Get or Create a build job based on the params.

    If a build job already exists, then we check if the build has already an image created.
    If the image does not exists, and the job is already done we force create a new job.

    Returns:
        tuple: (build_job, image_exists[bool], build_status[bool])
    """
    build_job, rebuild = BuildJob.create(
        user=user,
        project=project,
        config=config,
        code_reference=code_reference,
        configmap_refs=configmap_refs,
        secret_refs=secret_refs)

    if build_job.succeeded and not rebuild:
        # Check if image was built in less than an 6 hours
        return build_job, True, False

    if check_image(build_job=build_job):
        # Check if image exists already
        return build_job, True, False

    if build_job.is_done:
        build_job, _ = BuildJob.create(
            user=user,
            project=project,
            config=config,
            code_reference=code_reference,
            configmap_refs=configmap_refs,
            secret_refs=secret_refs,
            nocache=True)

    if not build_job.is_running:
        # We need to build the image first
        auditor.record(event_type=BUILD_JOB_STARTED_TRIGGERED,
                       instance=build_job,
                       actor_id=user.id,
                       actor_name=user.username)
        build_status = start_dockerizer(build_job=build_job)
    else:
        build_status = True

    return build_job, False, build_status


def start_dockerizer(build_job):
    # Update job status to show that its started
    build_job.set_status(JobLifeCycle.SCHEDULED)

    spawner = DockerizerSpawner(
        project_name=build_job.project.unique_name,
        project_uuid=build_job.project.uuid.hex,
        job_name=build_job.unique_name,
        job_uuid=build_job.uuid.hex,
        k8s_config=settings.K8S_CONFIG,
        namespace=settings.K8S_NAMESPACE,
        in_cluster=True)

    error = {}
    try:
        results = spawner.start_dockerizer(resources=build_job.resources,
                                           node_selector=build_job.node_selector,
                                           affinity=build_job.affinity,
                                           tolerations=build_job.tolerations)
        auditor.record(event_type=BUILD_JOB_STARTED,
                       instance=build_job)
        build_job.definition = get_job_definition(results)
        build_job.save(update_fields=['definition'])
        return True
    except ApiException:
        _logger.error('Could not start build job, please check your polyaxon spec',
                      exc_info=True)
        error = {
            'raised': True,
            'traceback': traceback.format_exc(),
            'message': 'Could not start build job, encountered a Kubernetes ApiException.'
        }
    except VolumeNotFoundError as e:
        _logger.error('Could not start build job, please check your volume definitions.',
                      exc_info=True)
        error = {
            'raised': True,
            'traceback': traceback.format_exc(),
            'message': 'Could not start build job, encountered a volume definition problem. %s' % e
        }
    except Exception as e:
        _logger.error('Could not start build job, please check your polyaxon spec.',
                      exc_info=True)
        error = {
            'raised': True,
            'traceback': traceback.format_exc(),
            'message': 'Could not start build job encountered an {} exception.'.format(
                e.__class__.__name__
            )
        }
    finally:
        if error.get('raised'):
            build_job.set_status(
                JobLifeCycle.FAILED,
                message=error.get('message'),
                traceback=error.get('traceback'))


def stop_dockerizer(project_name, project_uuid, build_job_name, build_job_uuid):
    spawner = DockerizerSpawner(
        project_name=project_name,
        project_uuid=project_uuid,
        job_name=build_job_name,
        job_uuid=build_job_uuid,
        k8s_config=settings.K8S_CONFIG,
        namespace=settings.K8S_NAMESPACE,
        in_cluster=True)

    return spawner.stop_dockerizer()
