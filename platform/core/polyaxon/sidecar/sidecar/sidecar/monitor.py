import ocular

from ocular.constants import pod_statuses
from polyaxon_schemas.pod import PodLifeCycle


def is_container_terminated(status, container_id):
    container_statuses = status.get('container_statuses') or []
    statuses_by_name = ocular.processor.get_container_statuses_by_name(container_statuses)
    statuses = ocular.processor.get_container_status(statuses_by_name, (container_id,))
    statuses = statuses or {}
    return statuses.get('state', {}).get('terminated')


def get_status(event, container_id):
    pod_details = ocular.processor.get_pod_details(event_type='', event=event)
    return ocular.processor.get_job_status(pod_details, [container_id])[0]


def get_restart_count(status, container_id):
    container_statuses = status.get('container_statuses') or []
    if not container_statuses:
        return 0
    for container_status in container_statuses:
        if container_status['name'] != container_id:
            continue
        return container_status['restart_count'] or 0
    return 0


def is_pod_running(k8s_manager, pod_id, container_id, max_restarts):
    event = k8s_manager.k8s_api.read_namespaced_pod_status(pod_id, k8s_manager.namespace)
    event = event.to_dict()
    event_status = event.get('status', {})
    is_terminated = is_container_terminated(status=event_status, container_id=container_id)
    restart_count = get_restart_count(status=event_status, container_id=container_id)
    status = get_status(event=event, container_id=container_id)
    if status == pod_statuses.FAILED and restart_count < max_restarts:
        return True, status
    return (event_status.get('phase') in {PodLifeCycle.RUNNING,
                                          PodLifeCycle.PENDING,
                                          PodLifeCycle.CONTAINER_CREATING} and
            not is_terminated), status
