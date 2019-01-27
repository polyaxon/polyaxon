from typing import Iterable

import conf

from constants.k8s_jobs import EXPERIMENT_JOB_NAME_FORMAT
from logs_handlers.log_queries import base
from logs_handlers.log_queries.experiment_job import process_logs as process_experiment_job_logs
from logs_handlers.utils import safe_log_experiment
from polyaxon_k8s.manager import K8SManager
from schemas.tasks import TaskType


def stream_logs(experiment: 'Experiment') -> Iterable[str]:
    pod_id = EXPERIMENT_JOB_NAME_FORMAT.format(
        task_type=TaskType.MASTER,  # We default to master
        task_idx=0,
        experiment_uuid=experiment.uuid.hex)
    k8s_manager = K8SManager(namespace=conf.get('K8S_NAMESPACE'), in_cluster=True)
    return base.stream_logs(k8s_manager=k8s_manager,
                            pod_id=pod_id,
                            container_job_name=conf.get('CONTAINER_NAME_EXPERIMENT_JOB'))


def process_logs(experiment: 'Experiment', temp: bool = True) -> None:
    pod_id = EXPERIMENT_JOB_NAME_FORMAT.format(
        task_type=TaskType.MASTER,  # We default to master
        task_idx=0,
        experiment_uuid=experiment.uuid.hex)
    k8s_manager = K8SManager(namespace=conf.get('K8S_NAMESPACE'), in_cluster=True)
    log_lines = base.process_logs(k8s_manager=k8s_manager,
                                  pod_id=pod_id,
                                  container_job_name=conf.get('CONTAINER_NAME_EXPERIMENT_JOB'))

    safe_log_experiment(experiment_name=experiment.unique_name,
                        log_lines=log_lines,
                        temp=temp,
                        append=False)


def process_experiment_jobs_logs(experiment: 'Experiment', temp: bool = True) -> None:
    k8s_manager = K8SManager(namespace=conf.get('K8S_NAMESPACE'), in_cluster=True)
    for experiment_job in experiment.jobs.all():
        process_experiment_job_logs(experiment_job=experiment_job,
                                    temp=temp,
                                    k8s_manager=k8s_manager)
