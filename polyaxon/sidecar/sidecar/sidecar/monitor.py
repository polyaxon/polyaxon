import ocular

from polyaxon_schemas.pod import PodLifeCycle


def is_container_terminated(event, container_id):
    statuses_by_name = ocular.processor.get_container_statuses_by_name(
        event.status.to_dict().get('container_statuses', []))
    statuses = ocular.processor.get_container_status(statuses_by_name, (container_id,))
    return statuses.get('state', {}).get('terminated')


def is_pod_running(k8s_manager, pod_id, container_id):
    event = k8s_manager.k8s_api.read_namespaced_pod_status(pod_id, k8s_manager.namespace)
    is_terminated = is_container_terminated(event=event, container_id=container_id)
    return (
        event.status.phase in {PodLifeCycle.RUNNING,
                               PodLifeCycle.PENDING,
                               PodLifeCycle.CONTAINER_CREATING}and
        not is_terminated
    )
