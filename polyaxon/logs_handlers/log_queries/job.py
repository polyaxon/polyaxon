from django.conf import settings

from constants.k8s_jobs import JOB_NAME, JOB_NAME_FORMAT
from logs_handlers.log_queries import base
from logs_handlers.utils import safe_log_job
from polyaxon_k8s.manager import K8SManager


def stream_logs(pod_id):
    k8s_manager = K8SManager(namespace=settings.K8S_NAMESPACE, in_cluster=True)
    return base.stream_logs(k8s_manager=k8s_manager,
                            pod_id=pod_id,
                            container_job_name=settings.CONTAINER_NAME_JOB)


def process_logs(job, temp=True):
    pod_id = JOB_NAME_FORMAT.format(name=JOB_NAME, job_uuid=job.uuid.hex)
    k8s_manager = K8SManager(namespace=settings.K8S_NAMESPACE, in_cluster=True)
    log_lines = base.process_logs(k8s_manager=k8s_manager,
                                  pod_id=pod_id,
                                  container_job_name=settings.CONTAINER_NAME_JOB)

    safe_log_job(job_name=job.unique_name, log_lines=log_lines, temp=temp, append=False)
