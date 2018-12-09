from django.conf import settings

from polyaxon_k8s.manager import K8SManager

from logs_handlers.log_queries import base
from logs_handlers.utils import safe_log_experiment


def stream_logs(pod_id):
    k8s_manager = K8SManager(namespace=settings.K8S_NAMESPACE, in_cluster=True)
    return base.stream_logs(k8s_manager=k8s_manager,
                            pod_id=pod_id,
                            container_job_name=settings.CONTAINER_NAME_EXPERIMENT_JOB)


def process_logs(pod_id, experiment_name, temp=True):
    k8s_manager = K8SManager(namespace=settings.K8S_NAMESPACE, in_cluster=True)
    log_lines = base.process_logs(k8s_manager=k8s_manager,
                                  pod_id=pod_id,
                                  container_job_name=settings.CONTAINER_NAME_EXPERIMENT_JOB)

    safe_log_experiment(experiment_name=experiment_name, log_lines=log_lines, temp=temp)
