import logging

from polyaxon_schemas.pod import PodLifeCycle

logger = logging.getLogger('polyaxon.monitors.sidecar')


def is_running(k8s_manager, pod_id):
    status = k8s_manager.k8s_api.read_namespaced_pod_status(pod_id,
                                                            k8s_manager.namespace)
    return status.status.phase == PodLifeCycle.RUNNING
