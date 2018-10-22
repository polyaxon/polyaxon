import logging
import time

from hestia.logging_utils import LogSpec

from constants.pods import PodLifeCycle
from schemas.job_labels import JobLabelConfig
from sidecarv2 import settings

logger = logging.getLogger('polyaxon.monitors.sidecar')


def _handle_log_stream(stream, publish):
    log_lines = []
    last_emit_time = time.time()
    for log_line in stream:
        log_lines.append(log_line.decode('utf-8').strip())
        publish_cond = (
            len(log_lines) == settings.MESSAGES_COUNT or
            (log_lines and time.time() - last_emit_time > settings.MESSAGES_TIMEOUT_SHORT)
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
        log_lines = [LogSpec(log_line=log_line, name='{}.{}'.format(task_type, int(task_idx) + 1))
                     for log_line in log_lines]
        publisher.publish_experiment_job_log(
            log_lines=log_lines,
            experiment_uuid=experiment_uuid,
            experiment_name=experiment_name,
            job_uuid=job_uuid)

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
        log_lines = [LogSpec(log_line=log_line) for log_line in log_lines]
        publisher.publish_job_log(
            log_lines=log_lines,
            job_name=job_name,
            job_uuid=job_uuid)

    _handle_log_stream(stream=raw.stream(), publish=publish)


def can_log(k8s_manager, pod_id, log_sleep_interval):
    status = k8s_manager.k8s_api.read_namespaced_pod_status(pod_id,
                                                            k8s_manager.namespace)
    labels = status.metadata.labels
    while (status.status.phase != PodLifeCycle.RUNNING and
           status.status.phase not in PodLifeCycle.DONE_STATUS):
        time.sleep(log_sleep_interval)
        status = k8s_manager.k8s_api.read_namespaced_pod_status(pod_id,
                                                                k8s_manager.namespace)
        labels = status.metadata.labels

    return status.status.phase == PodLifeCycle.RUNNING, JobLabelConfig.from_dict(labels)
