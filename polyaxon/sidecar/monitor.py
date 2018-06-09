import logging
import time

import publisher

from constants.experiments import ExperimentLifeCycle
from constants.pods import PodLifeCycle
from polyaxon_schemas.experiment import JobLabelConfig

logger = logging.getLogger(__name__)


def _handle_log_stream(stream, publish):
    log_lines = []
    last_emit_time = time.time()
    for log_line in stream:
        log_lines.append(log_line)
        publish_cond = (
            len(log_lines) == publisher.MESSAGES_COUNT or
            (log_lines and time.time() - last_emit_time > publisher.MESSAGES_TIMEOUT)
        )
        if publish_cond:
            publish(log_lines)
            log_lines = []
            last_emit_time = time.time()
    if log_lines:
        publish(log_lines)


def run_for_experiment_job(k8s_manager,
                           pod_id,
                           experiment_uuid,
                           experiment_name,
                           job_uuid,
                           task_type,
                           task_idx,
                           container_job_name):
    raw = k8s_manager.k8s_api.read_namespaced_pod_log(
        pod_id,
        k8s_manager.namespace,
        container=container_job_name,
        follow=True,
        _preload_content=False)

    def publish(log_lines):
        publisher.publish_experiment_job_log(
            log_lines=log_lines,
            status=ExperimentLifeCycle.RUNNING,
            experiment_uuid=experiment_uuid,
            experiment_name=experiment_name,
            job_uuid=job_uuid,
            task_type=task_type,
            task_idx=task_idx)

    _handle_log_stream(stream=raw.stream(), publish=publish)


def run_for_job(k8s_manager,
                pod_id,
                job_name,
                job_uuid,
                container_job_name):
    raw = k8s_manager.k8s_api.read_namespaced_pod_log(
        pod_id,
        k8s_manager.namespace,
        container=container_job_name,
        follow=True,
        _preload_content=False)

    def publish(log_lines):
        publisher.publish_job_log(
            log_lines=log_lines,
            job_name=job_name,
            job_uuid=job_uuid)

    _handle_log_stream(stream=raw.stream(), publish=publish)


def can_log(k8s_manager, pod_id, log_sleep_interval):
    status = k8s_manager.k8s_api.read_namespaced_pod_status(pod_id,
                                                            k8s_manager.namespace)
    logger.debug(status)
    labels = status.metadata.labels
    while (status.status.phase != PodLifeCycle.RUNNING and
           status.status.phase not in PodLifeCycle.DONE_STATUS):
        time.sleep(log_sleep_interval)
        status = k8s_manager.k8s_api.read_namespaced_pod_status(pod_id,
                                                                k8s_manager.namespace)
        labels = status.metadata.labels

    return status.status.phase == PodLifeCycle.RUNNING, JobLabelConfig.from_dict(labels)
