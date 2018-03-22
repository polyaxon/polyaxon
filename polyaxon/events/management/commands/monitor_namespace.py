import time

from django.conf import settings

from kubernetes.client.rest import ApiException

from polyaxon_k8s.manager import K8SManager

from clusters.models import Cluster
from events.management.commands._base_monitor import BaseMonitorCommand
from events.monitors import namespace


class Command(BaseMonitorCommand):
    help = 'Watch namespace warning and errors events.'

    def handle(self, *args, **options):
        log_sleep_interval = options['log_sleep_interval']
        self.stdout.write(
            "Started a new namespace monitor with, "
            "log sleep interval: `{}`.".format(log_sleep_interval),
            ending='\n')
        k8s_manager = K8SManager(namespace=settings.K8S_NAMESPACE, in_cluster=True)
        cluster = Cluster.load()
        while True:
            try:
                namespace.run(k8s_manager, cluster)
            except ApiException as e:
                namespace.logger.error(
                    "Exception when calling CoreV1Api->list_event_for_all_namespaces: %s\n" % e)
                time.sleep(log_sleep_interval)
            except Exception as e:
                namespace.logger.exception("Unhandled exception occurred: %s\n" % e)
