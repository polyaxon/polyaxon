import logging
import time

import publisher

from constants.experiments import ExperimentLifeCycle
from constants.pods import PodLifeCycle
from polyaxon_schemas.experiment import JobLabelConfig

logger = logging.getLogger(__name__)


def run(k8s_manager,
        pod_id,
        experiment_uuid,
        experiment_name,
        job_uuid,
        task_type,
        task_idx,
        container_job_name):
    raw = k8s_manager.k8s_api.read_namespaced_pod_log(pod_id,
                                                      k8s_manager.namespace,
                                                      container=container_job_name,
                                                      follow=True,
                                                      _preload_content=False)
    for log_line in raw.stream():
        publisher.publish_experiment_log(log_line=log_line,
                                         status=ExperimentLifeCycle.RUNNING,
                                         experiment_uuid=experiment_uuid,
                                         experiment_name=experiment_name,
                                         job_uuid=job_uuid,
                                         task_type=task_type,
                                         task_idx=task_idx)


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
