import time

from kubernetes.client.rest import ApiException

from django.db import InterfaceError, connection
from urllib3.exceptions import MaxRetryError

import conf

from libs.base_monitor import BaseMonitorCommand
from monitor_statuses import monitor
from options.registry.k8s import K8S_NAMESPACE
from polyaxon_k8s.manager import K8SManager


class Command(BaseMonitorCommand):
    help = 'Watch jobs statuses events.'

    def handle(self, *args, **options) -> None:
        sleep_interval = options['sleep_interval']
        time.sleep(sleep_interval)
        self.stdout.write(
            "Started a new statuses monitor with, "
            "log sleep interval: `{}`.".format(sleep_interval),
            ending='\n')
        k8s_manager = K8SManager(namespace=conf.get(K8S_NAMESPACE), in_cluster=True)
        while True:
            try:
                monitor.run(k8s_manager)
            except (ApiException, ValueError, MaxRetryError) as e:
                monitor.logger.warning(
                    "Exception when calling CoreV1Api->list_namespaced_pod: %s\n", e)
                time.sleep(sleep_interval)
            except InterfaceError:
                # In some cases such as timeout, database restart, connection will
                # be closed by remote peer. Django cannot recover from this
                # condition automatically. Here we close dead connection manually,
                # make Django to reconnect next time querying DB.
                connection.close()
                monitor.logger.warning(
                    "Database connection is already closed by peer, discard old connection\n")
                time.sleep(sleep_interval)
            except Exception as e:
                monitor.logger.exception("Unhandled exception occurred %s\n", e)
