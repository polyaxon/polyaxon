from django.conf import settings

from constants.k8s_jobs import EXPERIMENT_JOB_NAME_FORMAT
from logs_handlers.log_queries import base
from logs_handlers.utils import safe_log_experiment_job
from polyaxon_k8s.manager import K8SManager


def stream_logs(pod_id, task_type, task_id):
    k8s_manager = K8SManager(namespace=settings.K8S_NAMESPACE, in_cluster=True)
    return base.stream_logs(k8s_manager=k8s_manager,
                            pod_id=pod_id,
                            container_job_name=settings.CONTAINER_NAME_EXPERIMENT_JOB,
                            task_type=task_type,
                            task_idx=task_id)


def process_logs(experiment_job, temp=True, k8s_manager=None):
    task_type = experiment_job.role
    task_id = experiment_job.sequence
    pod_id = EXPERIMENT_JOB_NAME_FORMAT.format(
        task_type=task_type,  # We default to master
        task_idx=task_id,
        experiment_uuid=experiment_job.experiment.uuid.hex)
    if not k8s_manager:
        k8s_manager = K8SManager(namespace=settings.K8S_NAMESPACE, in_cluster=True)
    log_lines = base.process_logs(k8s_manager=k8s_manager,
                                  pod_id=pod_id,
                                  container_job_name=settings.CONTAINER_NAME_EXPERIMENT_JOB,
                                  task_type=task_type,
                                  task_idx=task_id)

    safe_log_experiment_job(experiment_job_name=experiment_job.unique_name,
                            log_lines=log_lines,
                            temp=temp)
