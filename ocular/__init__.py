import logging

from hestia.tz_utils import now

from kubernetes import watch

from ocular.processor import get_pod_state

logger = logging.getLogger('ocular')


def monitor(k8s_api, namespace, container_names, label_selector=None):
    w = watch.Watch()

    for event in w.stream(k8s_api.list_namespaced_pod,
                          namespace=namespace,
                          label_selector=label_selector):
        created_at = now()
        logger.debug("Received event: %s", event['type'])
        event_object = event['object'].to_dict()
        logger.debug(event_object)
        yield get_pod_state(
            event_type=event['type'],
            event=event_object,
            job_container_names=container_names,
            created_at=created_at)
