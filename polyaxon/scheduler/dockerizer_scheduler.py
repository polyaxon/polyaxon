import logging
import traceback

from kubernetes.client.rest import ApiException

import auditor
import conf

from db.models.build_jobs import BuildJob
from events.registry.build_job import BUILD_JOB_STARTED, BUILD_JOB_STARTED_TRIGGERED
from libs.unique_urls import get_build_reconcile_url
from lifecycles.jobs import JobLifeCycle
from options.registry.build_jobs import BUILD_JOBS_BACKEND
from options.registry.deployments import CHART_VERSION
from options.registry.k8s import K8S_CONFIG, K8S_NAMESPACE
from options.registry.restarts import MAX_RESTARTS_BUILD_JOBS
from polypod.dockerizer import DockerizerSpawner
from polypod.kaniko import KanikoSpawner
from polypod.templates.restart_policy import get_max_restart
from registry.exceptions import ContainerRegistryError
from registry.image_info import get_image_name
from registry.registry_context import get_registry_context
from scheduler.utils import get_job_definition
from schemas import BuildBackend
from stores.exceptions import StoreNotFoundError

_logger = logging.getLogger('polyaxon.scheduler.dockerizer')


def create_build_job(user, project, config, code_reference, config_map_refs=None, secret_refs=None):
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
        config_map_refs=config_map_refs,
        secret_refs=secret_refs)

    if build_job.succeeded and not rebuild:
        return build_job, True, False

    if build_job.is_done:
        build_job, _ = BuildJob.create(
            user=user,
            project=project,
            config=config,
            code_reference=code_reference,
            config_map_refs=config_map_refs,
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


def get_default_spawner():
    if conf.get(BUILD_JOBS_BACKEND) == BuildBackend.NATIVE:
        return DockerizerSpawner
    elif conf.get(BUILD_JOBS_BACKEND) == BuildBackend.KANIKO:
        return KanikoSpawner
    return DockerizerSpawner


def get_spawner_class(builder):
    if builder == BuildBackend.NATIVE:
        return DockerizerSpawner
    elif builder == BuildBackend.KANIKO:
        return KanikoSpawner
    return get_default_spawner()


def start_dockerizer(build_job):
    # Update job status to show that its started
    build_job.set_status(JobLifeCycle.SCHEDULED)
    spawner_class = get_spawner_class(build_job.backend)

    try:
        registry_spec = get_registry_context(build_backend=build_job.backend)
    except ContainerRegistryError:
        build_job.set_status(
            JobLifeCycle.FAILED,
            message='Could not start the dockerizer job, please check your registry configuration.')
        return

    spawner = spawner_class(
        project_name=build_job.project.unique_name,
        project_uuid=build_job.project.uuid.hex,
        job_name=build_job.unique_name,
        job_uuid=build_job.uuid.hex,
        k8s_config=conf.get(K8S_CONFIG),
        namespace=conf.get(K8S_NAMESPACE),
        version=conf.get(CHART_VERSION),
        in_cluster=True,
        use_sidecar=True,
        log_level=build_job.specification.log_level)

    error = {}
    try:
        results = spawner.start_dockerizer(
            commit=build_job.commit,
            from_image=build_job.build_image,
            dockerfile_path=build_job.build_dockerfile,
            context_path=build_job.build_context,
            image_tag=build_job.uuid.hex,
            image_name=get_image_name(
                build_job=build_job,
                registry_host=registry_spec.host),
            build_steps=build_job.build_steps,
            env_vars=build_job.build_env_vars,
            lang_env=build_job.build_lang_env,
            nocache=build_job.build_nocache,
            insecure=registry_spec.insecure,
            creds_secret_ref=registry_spec.secret,
            creds_secret_items=registry_spec.secret_items,
            secret_refs=build_job.secret_refs,
            config_map_refs=build_job.config_map_refs,
            resources=build_job.resources,
            labels=build_job.labels,
            annotations=build_job.annotations,
            node_selector=build_job.node_selector,
            affinity=build_job.affinity,
            tolerations=build_job.tolerations,
            max_restarts=get_max_restart(build_job.max_restarts, conf.get(MAX_RESTARTS_BUILD_JOBS)),
            reconcile_url=get_build_reconcile_url(build_job.unique_name))
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
    except StoreNotFoundError as e:
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
        k8s_config=conf.get(K8S_CONFIG),
        namespace=conf.get(K8S_NAMESPACE),
        in_cluster=True)

    return spawner.stop_dockerizer()
