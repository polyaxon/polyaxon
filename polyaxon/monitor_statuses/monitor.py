import logging

from typing import Mapping

import conf
import ocular
import workers

from constants.experiment_jobs import get_experiment_job_uuid
from db.redis.containers import RedisJobContainers
from lifecycles.jobs import JobLifeCycle
from options.registry.container_names import (
    CONTAINER_NAME_BUILD_JOBS,
    CONTAINER_NAME_EXPERIMENT_JOBS,
    CONTAINER_NAME_JOBS,
    CONTAINER_NAME_PLUGIN_JOBS,
    CONTAINER_NAME_PYTORCH_JOBS,
    CONTAINER_NAME_TF_JOBS
)
from options.registry.k8s import K8S_NAMESPACE
from options.registry.spawner import (
    APP_LABELS_DOCKERIZER,
    APP_LABELS_EXPERIMENT,
    APP_LABELS_JOB,
    APP_LABELS_NOTEBOOK,
    APP_LABELS_TENSORBOARD,
    ROLE_LABELS_DASHBOARD,
    ROLE_LABELS_WORKER,
    TYPE_LABELS_RUNNER
)
from options.registry.ttl import TTL_WATCH_STATUSES
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
        conf.get(ROLE_LABELS_WORKER),
        conf.get(ROLE_LABELS_DASHBOARD),
        conf.get(TYPE_LABELS_RUNNER))


def handle_experiment_job_condition(event_object, pod_state, status, labels, container_name):
    update_job_containers(event_object, status, container_name)
    logger.debug("Sending state to handler %s, %s", status, labels)
    # Handle experiment job statuses
    workers.send(
        K8SEventsCeleryTasks.K8S_EVENTS_HANDLE_EXPERIMENT_JOB_STATUSES,
        kwargs={'payload': pod_state},
        countdown=None)


def run(k8s_manager: 'K8SManager') -> None:
    for (event_object, pod_state) in ocular.monitor(k8s_manager.k8s_api,
                                                    namespace=conf.get(K8S_NAMESPACE),
                                                    container_names=(
                                                        conf.get(CONTAINER_NAME_EXPERIMENT_JOBS),
                                                        conf.get(CONTAINER_NAME_TF_JOBS),
                                                        conf.get(CONTAINER_NAME_PYTORCH_JOBS),
                                                        conf.get(CONTAINER_NAME_PLUGIN_JOBS),
                                                        conf.get(CONTAINER_NAME_JOBS),
                                                        conf.get(CONTAINER_NAME_BUILD_JOBS)),
                                                    label_selector=get_label_selector(),
                                                    return_event=True,
                                                    watch_ttl=conf.get(TTL_WATCH_STATUSES)):
        logger.debug('-------------------------------------------\n%s\n', pod_state)
        if not pod_state:
            continue

        status = pod_state['status']
        labels = None
        if pod_state['details'] and pod_state['details']['labels']:
            labels = pod_state['details']['labels']
        logger.info("Updating job container %s, %s", status, labels)

        experiment_condition = status and labels['app'] == conf.get(APP_LABELS_EXPERIMENT)

        experiment_job_condition = (
            conf.get(CONTAINER_NAME_EXPERIMENT_JOBS) in pod_state['details']['container_statuses']
            or 'job_uuid' in labels
        )

        tf_job_condition = (
            conf.get(CONTAINER_NAME_TF_JOBS) in pod_state['details']['container_statuses']
            or 'tf-replica-index' in labels
        )

        mpi_job_condition = 'mpi_job_name' in labels

        pytorch_job_condition = (
            conf.get(CONTAINER_NAME_PYTORCH_JOBS) in pod_state['details']['container_statuses']
            or 'pytroch-replica-index' in labels
        )

        job_condition = (
            conf.get(CONTAINER_NAME_JOBS) in pod_state['details']['container_statuses'] or
            (status and labels['app'] == conf.get(APP_LABELS_JOB))
        )

        plugin_job_condition = (
            conf.get(CONTAINER_NAME_PLUGIN_JOBS) in pod_state['details']['container_statuses'] or
            (status and
             labels['app'] in (conf.get(APP_LABELS_TENSORBOARD), conf.get(APP_LABELS_NOTEBOOK)))
        )

        dockerizer_job_condition = (
            conf.get(CONTAINER_NAME_BUILD_JOBS) in pod_state['details']['container_statuses']
            or (status and labels['app'] == conf.get(APP_LABELS_DOCKERIZER))
        )

        if experiment_condition:
            if tf_job_condition:
                # We augment the payload with standard Polyaxon requirement
                pod_state['details']['labels']['job_uuid'] = get_experiment_job_uuid(
                    experiment_uuid=labels['experiment_uuid'],
                    task_type=labels['task_type'],
                    task_index=labels['tf-replica-index']
                )
                handle_experiment_job_condition(
                    event_object=event_object,
                    pod_state=pod_state,
                    status=status,
                    labels=labels,
                    container_name=conf.get(CONTAINER_NAME_TF_JOBS))

            elif pytorch_job_condition:
                # We augment the payload with standard Polyaxon requirement
                pod_state['details']['labels']['job_uuid'] = get_experiment_job_uuid(
                    experiment_uuid=labels['experiment_uuid'],
                    task_type=labels['task_type'],
                    task_index=labels['pytorch-replica-index']
                )
                handle_experiment_job_condition(
                    event_object=event_object,
                    pod_state=pod_state,
                    status=status,
                    labels=labels,
                    container_name=conf.get(CONTAINER_NAME_PYTORCH_JOBS))

            elif mpi_job_condition:
                job_name = pod_state['details']['pod_name']
                parts = job_name.split('-')
                if len(parts) != 4:
                    continue

                # We augment the payload with standard Polyaxon requirement
                pod_state['details']['labels']['job_uuid'] = get_experiment_job_uuid(
                    experiment_uuid=labels['experiment_uuid'],
                    task_type=labels['task_type'],
                    task_index=parts[-1]
                )

                handle_experiment_job_condition(
                    event_object=event_object,
                    pod_state=pod_state,
                    status=status,
                    labels=labels,
                    container_name=conf.get(CONTAINER_NAME_EXPERIMENT_JOBS))

            elif experiment_job_condition:
                handle_experiment_job_condition(
                    event_object=event_object,
                    pod_state=pod_state,
                    status=status,
                    labels=labels,
                    container_name=conf.get(CONTAINER_NAME_EXPERIMENT_JOBS))

        elif job_condition:
            update_job_containers(event_object, status, conf.get(CONTAINER_NAME_JOBS))
            logger.debug("Sending state to handler %s, %s", status, labels)
            # Handle experiment job statuses
            workers.send(
                K8SEventsCeleryTasks.K8S_EVENTS_HANDLE_JOB_STATUSES,
                kwargs={'payload': pod_state},
                countdown=None)

        elif plugin_job_condition:
            logger.debug("Sending state to handler %s, %s", status, labels)
            # Handle plugin job statuses
            workers.send(
                K8SEventsCeleryTasks.K8S_EVENTS_HANDLE_PLUGIN_JOB_STATUSES,
                kwargs={'payload': pod_state},
                countdown=None)

        elif dockerizer_job_condition:
            logger.debug("Sending state to handler %s, %s", status, labels)
            # Handle dockerizer job statuses
            workers.send(
                K8SEventsCeleryTasks.K8S_EVENTS_HANDLE_BUILD_JOB_STATUSES,
                kwargs={'payload': pod_state},
                countdown=None)
        else:
            logger.info("Lost state %s, %s", status, pod_state)
