from hestia.logging_utils import LogSpec


def query_logs(k8s_manager, pod_id, container_job_name, stream=False):
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
        **params)


def process_log_line(log_line, task_type=None, task_idx=None):
    name = ''
    if task_type is not None and task_idx is not None:
        name = '{}.{}'.format(task_type, int(task_idx) + 1)

    return LogSpec(log_line=log_line.decode('utf-8').strip(), name=name)


def stream_logs(k8s_manager, pod_id, container_job_name, task_type=None, task_idx=None):
    raw = query_logs(k8s_manager=k8s_manager,
                     pod_id=pod_id,
                     container_job_name=container_job_name,
                     stream=True)
    for log_line in raw.stream():
        yield process_log_line(log_line=log_line, task_type=task_type, task_idx=task_idx)


def process_logs(k8s_manager, pod_id, container_job_name, task_type=None, task_idx=None):
    logs = query_logs(k8s_manager=k8s_manager,
                      pod_id=pod_id,
                      container_job_name=container_job_name)
    log_lines = []
    for log_line in logs.split('\n'):
        log_lines.append(
            process_log_line(log_line=log_line, task_type=task_type, task_idx=task_idx))

    return log_lines
