import logging

from hestia.tz_utils import now
from kubernetes import watch

from ocular.processor import get_pod_state

logger = logging.getLogger('ocular')


def monitor(k8s_api, namespace, container_names, label_selector=None, return_event=False):
    w = watch.Watch()

    for event in w.stream(k8s_api.list_namespaced_pod,
                          namespace=namespace,
                          label_selector=label_selector):
        created_at = now()
        logger.debug("Received event: %s", event['type'])
        event_object = event['object'].to_dict()
        logger.debug("Event object: %s", event_object)
        pod_state = get_pod_state(
            event_type=event['type'],
            event=event_object,
            job_container_names=container_names,
            created_at=created_at)
        logger.debug("Pod state: %s", pod_state)
        if return_event:
            yield (event_object, pod_state)
        else:
            yield pod_state
