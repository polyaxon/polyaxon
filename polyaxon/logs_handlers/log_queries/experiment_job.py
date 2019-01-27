from typing import Iterable

import conf

from logs_handlers.log_queries import base
from logs_handlers.utils import safe_log_experiment_job
from polyaxon_k8s.manager import K8SManager


def stream_logs(pod_id: str, task_type: str, task_id: int) -> Iterable[str]:
    k8s_manager = K8SManager(namespace=conf.get('K8S_NAMESPACE'), in_cluster=True)
    return base.stream_logs(k8s_manager=k8s_manager,
                            pod_id=pod_id,
                            container_job_name=conf.get('CONTAINER_NAME_EXPERIMENT_JOB'),
                            task_type=task_type,
                            task_idx=task_id)


def process_logs(experiment_job: 'ExperimentJob',
                 temp: bool = True,
                 k8s_manager: 'K8SManager' = None) -> None:
    task_type = experiment_job.role
    task_id = experiment_job.sequence
    if not k8s_manager:
        k8s_manager = K8SManager(namespace=conf.get('K8S_NAMESPACE'), in_cluster=True)
    log_lines = base.process_logs(k8s_manager=k8s_manager,
                                  pod_id=experiment_job.pod_id,
                                  container_job_name=conf.get('CONTAINER_NAME_EXPERIMENT_JOB'),
                                  task_type=task_type,
                                  task_idx=task_id)

    safe_log_experiment_job(experiment_job_name=experiment_job.unique_name,
                            log_lines=log_lines,
                            temp=temp,
                            append=False)
