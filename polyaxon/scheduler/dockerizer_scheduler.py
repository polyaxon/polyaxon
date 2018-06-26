import logging

from kubernetes.client.rest import ApiException

from django.conf import settings
from django.utils.timezone import now

import auditor

from constants.jobs import JobLifeCycle
from db.models.build_jobs import BuildJob
from docker_images.image_info import get_tagged_image
from event_manager.events.build_job import BUILD_JOB_STARTED, BUILD_JOB_STARTED_TRIGGERED
from scheduler.spawners.dockerizer_spawner import DockerizerSpawner
from scheduler.spawners.templates.node_selectors import get_node_selector
from scheduler.spawners.utils import get_job_definition

_logger = logging.getLogger('polyaxon.scheduler.dockerizer')


def check_image(build_job):
    from docker import APIClient

    docker = APIClient(version='auto')
    return docker.images(get_tagged_image(build_job))


def create_build_job(user, project, config, code_reference):
    """Get or Create a build job based on the params.

    If a build job already exists, then we check if the build has already an image created.
    If the image does not exists, and the job is already done we force create a new job.

    Returns:
        tuple: (build_job, image_exists[bool], build_status[bool])
    """
    build_job = BuildJob.create(
        user=user,
        project=project,
        config=config,
        code_reference=code_reference)

    if check_image(build_job=build_job):
        # Check if image exists already
        return build_job, True, False

    if build_job.succeeded and (now() - build_job.finished_at).seconds < 3600 * 6:
        # Check if image was built in less than an 6 hours
        return build_job, True, False

    if build_job.is_done:
        build_job = BuildJob.create(
            user=user,
            project=project,
            config=config,
            code_reference=code_reference,
            nocache=True)

    if not build_job.is_running:
        # We need to build the image first
        auditor.record(event_type=BUILD_JOB_STARTED_TRIGGERED,
                       instance=build_job,
                       actor_id=user.id)
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
    try:
        node_selectors = get_node_selector(
            node_selector=build_job.node_selectors,
            default_node_selector=settings.NODE_SELECTORS_BUILDS)
        results = spawner.start_dockerizer(resources=build_job.resources,
                                           node_selectors=node_selectors)
        auditor.record(event_type=BUILD_JOB_STARTED,
                       instance=build_job)
    except ApiException as e:
        _logger.warning('Could not start build job, please check your polyaxon spec %s', e)
        build_job.set_status(
            JobLifeCycle.FAILED,
            message='Could not start build job, encountered a Kubernetes ApiException.')
        return False
    except Exception as e:
        _logger.warning('Could not start build job, please check your polyaxon spec %s', e)
        build_job.set_status(
            JobLifeCycle.FAILED,
            message='Could not start build job encountered an {} exception.'.format(
                e.__class__.__name__
            ))
        return False
    build_job.definition = get_job_definition(results)
    build_job.save()
    return True


def stop_dockerizer(project_name, project_uuid, build_job_name, build_job_uuid):
    spawner = DockerizerSpawner(
        project_name=project_name,
        project_uuid=project_uuid,
        job_name=build_job_name,
        job_uuid=build_job_uuid,
        k8s_config=settings.K8S_CONFIG,
        namespace=settings.K8S_NAMESPACE,
        in_cluster=True)

    spawner.stop_dockerizer()
