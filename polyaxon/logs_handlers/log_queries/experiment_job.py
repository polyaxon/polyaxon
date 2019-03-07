import conf

from constants.experiment_jobs import get_experiment_job_container_name
from logs_handlers.log_queries import base
from logs_handlers.utils import safe_log_experiment_job
from polyaxon_k8s.manager import K8SManager


def process_logs(experiment_job: 'ExperimentJob',
                 temp: bool = True,
                 k8s_manager: 'K8SManager' = None) -> None:
    task_type = experiment_job.role
    task_id = experiment_job.sequence
    if not k8s_manager:
        k8s_manager = K8SManager(namespace=conf.get('K8S_NAMESPACE'), in_cluster=True)
    container_job_name = get_experiment_job_container_name(
        backend=experiment_job.experiment.backend,
        framework=experiment_job.experiment.framework)
    log_lines = base.process_logs(k8s_manager=k8s_manager,
                                  pod_id=experiment_job.pod_id,
                                  container_job_name=container_job_name,
                                  task_type=task_type,
                                  task_idx=task_id)

    safe_log_experiment_job(experiment_job_name=experiment_job.unique_name,
                            log_lines=log_lines,
                            temp=temp,
                            append=False)
