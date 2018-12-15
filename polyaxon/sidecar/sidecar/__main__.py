import time

import argparse

from kubernetes.client.rest import ApiException

from polyaxon_client.client import PolyaxonClient

from polyaxon_k8s.manager import K8SManager

from sidecar.monitor import is_pod_running
from sidecar import settings

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--pod_id',
        type=str
    )
    parser.add_argument(
        '--app_label',
        type=str
    )
    parser.add_argument(
        '--container_id',
        type=str
    )
    parser.add_argument(
        '--log_sleep_interval',
        default=2,
        type=int
    )
    args = parser.parse_args()
    arguments = args.__dict__

    pod_id = arguments.pop('pod_id')
    container_id = arguments.pop('container_id')
    app_label = arguments.pop('app_label')
    log_sleep_interval = arguments.pop('log_sleep_interval')

    k8s_manager = K8SManager(namespace=settings.K8S_NAMESPACE, in_cluster=True)
    client = PolyaxonClient()
    client.set_internal_health_check()
    retry = 0
    is_running = True
    while is_running and retry < 3:
        time.sleep(log_sleep_interval)
        try:
            is_running = is_pod_running(k8s_manager, pod_id, container_id)
        except ApiException:
            retry += 1
            time.sleep(log_sleep_interval)  # We wait a bit more before try
