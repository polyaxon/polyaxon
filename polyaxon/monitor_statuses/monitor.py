import logging

from kubernetes import watch

from django.conf import settings

from constants.jobs import JobLifeCycle
from libs.redis_db import RedisJobContainers
from monitor_statuses.jobs import get_job_state
from polyaxon.celery_api import app as celery_app
from polyaxon.settings import EventsCeleryTasks

logger = logging.getLogger('polyaxon.monitors.statuses')


def update_job_containers(event, status, job_container_name):
    if JobLifeCycle.is_done(status):
        # Remove the job monitoring
        job_uuid = event['metadata']['labels']['job_uuid']
        logger.info('Stop monitoring job_uuid: %s', job_uuid)
        RedisJobContainers.remove_job(job_uuid)

    if event['status']['container_statuses'] is None:
        return

    def get_container_id(container_id):
        if not container_id:
            return None
        if container_id.startswith('docker://'):
            return container_id[len('docker://'):]
        return container_id

    for container_status in event['status']['container_statuses']:
        if container_status['name'] != job_container_name:
            continue

        container_id = get_container_id(container_status['container_id'])
        if container_id:
            job_uuid = event['metadata']['labels']['job_uuid']
            if container_status['state']['running'] is not None:
                logger.info('Monitoring (container_id, job_uuid): (%s, %s)',
                            container_id, job_uuid)
                RedisJobContainers.monitor(container_id=container_id, job_uuid=job_uuid)
            else:

                RedisJobContainers.remove_container(container_id=container_id)


def get_label_selector():
    type_label = settings.TYPE_LABELS_EXPERIMENT
    return 'role in ({},{}),type={}'.format(
        settings.ROLE_LABELS_WORKER,
        settings.ROLE_LABELS_DASHBOARD,
        type_label)


def run(k8s_manager):
    w = watch.Watch()

    for event in w.stream(k8s_manager.k8s_api.list_namespaced_pod,
                          namespace=k8s_manager.namespace,
                          label_selector=get_label_selector()):
        logger.debug("Received event: %s", event['type'])
        event_object = event['object'].to_dict()
        job_state = get_job_state(
            event_type=event['type'],
            event=event_object,
            job_container_names=(settings.CONTAINER_NAME_EXPERIMENT_JOB,
                                 settings.CONTAINER_NAME_PLUGIN_JOB,
                                 settings.CONTAINER_NAME_JOB,
                                 settings.CONTAINER_NAME_DOCKERIZER_JOB),
            experiment_type_label=settings.TYPE_LABELS_EXPERIMENT)

        if job_state:
            status = job_state.status
            labels = None
            if job_state.details and job_state.details.labels:
                labels = job_state.details.labels.to_dict()
            logger.info("Updating job container %s, %s", status, labels)
            logger.debug(event_object)
            job_state = job_state.to_dict()
            logger.debug(job_state)

            experiment_job_condition = (
                settings.CONTAINER_NAME_EXPERIMENT_JOB in job_state['details']['container_statuses']
            )

            job_condition = (
                settings.CONTAINER_NAME_JOB in job_state['details']['container_statuses']
            )

            plugin_job_condition = (
                settings.CONTAINER_NAME_PLUGIN_JOB in job_state['details']['container_statuses']
            )

            dockerizer_job_condition = (
                settings.CONTAINER_NAME_DOCKERIZER_JOB in job_state['details']['container_statuses']
            )

            if experiment_job_condition:
                update_job_containers(event_object, status, settings.CONTAINER_NAME_EXPERIMENT_JOB)
                # Handle experiment job statuses differently than plugin job statuses
                celery_app.send_task(
                    EventsCeleryTasks.EVENTS_HANDLE_EXPERIMENT_JOB_STATUSES,
                    kwargs={'payload': job_state})

            elif job_condition:
                update_job_containers(event_object, status, settings.CONTAINER_NAME_JOB)
                # Handle experiment job statuses differently than plugin job statuses
                celery_app.send_task(
                    EventsCeleryTasks.EVENTS_HANDLE_JOB_STATUSES,
                    kwargs={'payload': job_state})

            elif plugin_job_condition:
                # Handle plugin job statuses
                celery_app.send_task(
                    EventsCeleryTasks.EVENTS_HANDLE_PLUGIN_JOB_STATUSES,
                    kwargs={'payload': job_state})

            elif dockerizer_job_condition:
                # Handle dockerizer job statuses
                celery_app.send_task(
                    EventsCeleryTasks.EVENTS_HANDLE_BUILD_JOB_STATUSES,
                    kwargs={'payload': job_state})
