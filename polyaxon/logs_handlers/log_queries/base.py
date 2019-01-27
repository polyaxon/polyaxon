from typing import Any, Iterable

from hestia.logging_utils import LogSpec
from kubernetes.client.rest import ApiException

from polyaxon_k8s.exceptions import PolyaxonK8SError


def query_logs(k8s_manager: 'K8SManager',
               pod_id: str,
               container_job_name: str,
               stream: bool = False) -> Any:
    params = {}
    if stream:
        params = {
            'follow': True,
            '_preload_content': False
        }

    return k8s_manager.k8s_api.read_namespaced_pod_log(
        pod_id,
        k8s_manager.namespace,
        container=container_job_name,
        timestamps=True,
        **params)


def process_log_line(log_line: str, task_type: str = None, task_idx: int = None):
    name = ''
    if task_type is not None and task_idx is not None:
        name = '{}.{}'.format(task_type, int(task_idx) + 1)

    if not isinstance(log_line, str):
        log_line = log_line.decode('utf-8')

    return LogSpec(log_line=log_line.strip(), name=name)


def stream_logs(k8s_manager: 'K8SManager',
                pod_id: str,
                container_job_name: str,
                task_type: str = None,
                task_idx: int = None) -> Iterable[str]:
    raw = None
    retries = 0
    no_logs = True

    while retries < 3 and no_logs:
        try:
            raw = query_logs(k8s_manager=k8s_manager,
                             pod_id=pod_id,
                             container_job_name=container_job_name,
                             stream=True)
        except (PolyaxonK8SError, ApiException):
            retries += 1

    if not raw:
        yield ''
    else:
        for log_line in raw.stream():
            if log_line:
                yield process_log_line(log_line=log_line, task_type=task_type, task_idx=task_idx)


def process_logs(k8s_manager: 'K8SManager',
                 pod_id: str,
                 container_job_name: str,
                 task_type: str = None,
                 task_idx: int = None) -> str:
    logs = None
    retries = 0
    no_logs = True
    while retries < 3 and no_logs:
        try:
            logs = query_logs(k8s_manager=k8s_manager,
                              pod_id=pod_id,
                              container_job_name=container_job_name)
            no_logs = False
        except (PolyaxonK8SError, ApiException):
            retries += 1

    if not logs:
        return ''

    log_lines = []
    for log_line in logs.split('\n'):
        if log_line:
            log_lines.append(
                process_log_line(log_line=log_line, task_type=task_type, task_idx=task_idx))

    return '\n'.join(log_lines)
