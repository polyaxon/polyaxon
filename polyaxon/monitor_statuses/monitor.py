import logging

from typing import Mapping

import conf
import ocular

from constants.jobs import JobLifeCycle
from db.redis.containers import RedisJobContainers
from polyaxon.celery_api import celery_app
from polyaxon.settings import K8SEventsCeleryTasks

logger = logging.getLogger('polyaxon.monitors.statuses')


def update_job_containers(event: Mapping,
                          status: str,
                          job_container_name: str) -> None:
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


def get_label_selector() -> str:
    return 'role in ({},{}),type={}'.format(
        conf.get('ROLE_LABELS_WORKER'),
        conf.get('ROLE_LABELS_DASHBOARD'),
        conf.get('TYPE_LABELS_RUNNER'))


def run(k8s_manager: 'K8SManager') -> None:
    for (event_object, pod_state) in ocular.monitor(k8s_manager.k8s_api,
                                                    namespace=conf.get('K8S_NAMESPACE'),
                                                    container_names=(
                                                        conf.get('CONTAINER_NAME_EXPERIMENT_JOB'),
                                                        conf.get('CONTAINER_NAME_PLUGIN_JOB'),
                                                        conf.get('CONTAINER_NAME_JOB'),
                                                        conf.get('CONTAINER_NAME_DOCKERIZER_JOB')),
                                                    label_selector=get_label_selector(),
                                                    return_event=True,
                                                    watch_ttl=conf.get('TTL_WATCH_STATUSES')):
        logger.debug('-------------------------------------------\n%s\n', pod_state)
        if not pod_state:
            continue

        status = pod_state['status']
        labels = None
        if pod_state['details'] and pod_state['details']['labels']:
            labels = pod_state['details']['labels']
        logger.info("Updating job container %s, %s", status, labels)
        experiment_job_condition = (
            conf.get('CONTAINER_NAME_EXPERIMENT_JOB') in pod_state['details']['container_statuses']
            or (status and labels['app'] == conf.get('APP_LABELS_EXPERIMENT'))
        )

        job_condition = (
            conf.get('CONTAINER_NAME_JOB') in pod_state['details']['container_statuses'] or
            (status and labels['app'] == conf.get('APP_LABELS_JOB'))
        )

        plugin_job_condition = (
            conf.get('CONTAINER_NAME_PLUGIN_JOB') in pod_state['details']['container_statuses'] or
            (status and
             labels['app'] in (conf.get('APP_LABELS_TENSORBOARD'), conf.get('APP_LABELS_NOTEBOOK')))
        )

        dockerizer_job_condition = (
            conf.get('CONTAINER_NAME_DOCKERIZER_JOB') in pod_state['details']['container_statuses']
            or (status and labels['app'] == conf.get('APP_LABELS_DOCKERIZER'))
        )

        if experiment_job_condition:
            update_job_containers(event_object, status, conf.get('CONTAINER_NAME_EXPERIMENT_JOB'))
            logger.debug("Sending state to handler %s, %s", status, labels)
            # Handle experiment job statuses
            celery_app.send_task(
                K8SEventsCeleryTasks.K8S_EVENTS_HANDLE_EXPERIMENT_JOB_STATUSES,
                kwargs={'payload': pod_state})

        elif job_condition:
            update_job_containers(event_object, status, conf.get('CONTAINER_NAME_JOB'))
            logger.debug("Sending state to handler %s, %s", status, labels)
            # Handle experiment job statuses
            celery_app.send_task(
                K8SEventsCeleryTasks.K8S_EVENTS_HANDLE_JOB_STATUSES,
                kwargs={'payload': pod_state})

        elif plugin_job_condition:
            logger.debug("Sending state to handler %s, %s", status, labels)
            # Handle plugin job statuses
            celery_app.send_task(
                K8SEventsCeleryTasks.K8S_EVENTS_HANDLE_PLUGIN_JOB_STATUSES,
                kwargs={'payload': pod_state})

        elif dockerizer_job_condition:
            logger.debug("Sending state to handler %s, %s", status, labels)
            # Handle dockerizer job statuses
            celery_app.send_task(
                K8SEventsCeleryTasks.K8S_EVENTS_HANDLE_BUILD_JOB_STATUSES,
                kwargs={'payload': pod_state})
        else:
            logger.info("Lost state %s, %s", status, pod_state)
