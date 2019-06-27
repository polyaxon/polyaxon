import argparse
import time

from kubernetes.client.rest import ApiException

from polyaxon_client.client import PolyaxonClient
from polyaxon_k8s.manager import K8SManager
from sidecar import settings
from sidecar.monitor import is_pod_running

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--app_label',
        type=str
    )
    parser.add_argument(
        '--container_id',
        type=str
    )
    parser.add_argument(
        '--sleep_interval',
        default=2,
        type=int
    )
    parser.add_argument(
        '--max_restarts',
        default=0,
        type=int
    )
    args = parser.parse_args()
    arguments = args.__dict__

    container_id = arguments.pop('container_id')
    app_label = arguments.pop('app_label')
    sleep_interval = arguments.pop('sleep_interval')
    max_restarts = arguments.pop('max_restarts')

    k8s_manager = K8SManager(namespace=settings.K8S_NAMESPACE, in_cluster=True)
    client = PolyaxonClient()
    client.set_internal_health_check()
    retry = 0
    is_running = True
    status = None
    while is_running and retry < 3:
        time.sleep(sleep_interval)
        try:
            is_running, status = is_pod_running(k8s_manager,
                                                settings.POD_ID,
                                                container_id,
                                                max_restarts)
            print(is_running, status)
        except ApiException:
            retry += 1
            time.sleep(sleep_interval)  # We wait a bit more before try
