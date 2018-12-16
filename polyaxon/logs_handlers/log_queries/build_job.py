from django.conf import settings

from logs_handlers.log_queries import base
from logs_handlers.utils import safe_log_job
from polyaxon_k8s.manager import K8SManager


def stream_logs(build):
    k8s_manager = K8SManager(namespace=settings.K8S_NAMESPACE, in_cluster=True)
    return base.stream_logs(k8s_manager=k8s_manager,
                            pod_id=build.pod_id,
                            container_job_name=settings.CONTAINER_NAME_DOCKERIZER_JOB)


def process_logs(build, temp=True):
    k8s_manager = K8SManager(namespace=settings.K8S_NAMESPACE, in_cluster=True)
    log_lines = base.process_logs(k8s_manager=k8s_manager,
                                  pod_id=build.pod_id,
                                  container_job_name=settings.CONTAINER_NAME_DOCKERIZER_JOB)

    safe_log_job(job_name=build.unique_name, log_lines=log_lines, temp=temp, append=False)
