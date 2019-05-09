import logging
import time

from hestia.tz_utils import now
from kubernetes import watch
from kubernetes.client.rest import ApiException
from urllib3.exceptions import RequestError

from ocular.exceptions import OcularException
from ocular.processor import get_pod_state

logger = logging.getLogger('ocular')

LAST_SEEN = {'resource_version': None}


def _monitor(k8s_api, namespace, container_names, label_selector, watch_ttl):
    w = watch.Watch()
    start = time.time()

    params = {}
    if LAST_SEEN['resource_version']:
        params['resource_version'] = LAST_SEEN['resource_version']
    if watch_ttl:
        params['timeout_seconds'] = watch_ttl
    for event in w.stream(k8s_api.list_namespaced_pod,
                          namespace=namespace,
                          label_selector=label_selector,
                          **params):
        logger.debug("Received event: %s", event['type'])
        event_object = event['object'].to_dict()
        logger.debug("Event object: %s", event_object)
        LAST_SEEN['resource_version'] = event_object['metadata'].get('resource_version')
        created_at = now()
        try:
            pod_state = get_pod_state(
                event_type=event['type'],
                event=event_object,
                job_container_names=container_names,
                created_at=created_at)
            logger.debug("Pod state: %s", pod_state)
            yield (event_object, pod_state)

            if watch_ttl and time.time() - start > watch_ttl:
                logger.debug("Restarting watch process ...")
                w.stop()
                break
        except OcularException:
            pass


def monitor(k8s_api,
            namespace,
            container_names,
            label_selector='',
            return_event=False,
            watch_ttl=None,
            resource_version=None,
            sleep_interval=1):
    if resource_version:
        LAST_SEEN['resource_version'] = resource_version
    while True:
        try:
            for event_object, pod_state in _monitor(k8s_api,
                                                    namespace,
                                                    container_names,
                                                    label_selector,
                                                    watch_ttl):
                if return_event:
                    yield (event_object, pod_state)
                else:
                    yield pod_state
        except ApiException:
            time.sleep(sleep_interval)
        except RequestError:
            time.sleep(sleep_interval)
