import time

from kubernetes.client.rest import ApiException

from django.conf import settings
from django.db import InterfaceError, OperationalError, ProgrammingError

from db.models.clusters import Cluster
from event_monitors.management.commands._base_monitor import BaseMonitorCommand
from event_monitors.monitors import namespace
from polyaxon_k8s.manager import K8SManager


class Command(BaseMonitorCommand):
    help = 'Watch namespace warning and errors events.'

    def get_cluster_or_wait(self, log_sleep_interval):
        max_trials = 10
        trials = 0
        while trials < max_trials:
            try:
                return Cluster.load()
            except (InterfaceError, ProgrammingError, OperationalError) as e:
                namespace.logger.exception("Database is not synced yet %s\n", e)
                trials += 1
                time.sleep(log_sleep_interval * 2)
        return None

    def handle(self, *args, **options):
        log_sleep_interval = options['log_sleep_interval']
        self.stdout.write(
            "Started a new namespace monitor with, "
            "log sleep interval: `{}`.".format(log_sleep_interval),
            ending='\n')
        k8s_manager = K8SManager(namespace=settings.K8S_NAMESPACE, in_cluster=True)
        cluster = self.get_cluster_or_wait(log_sleep_interval)
        if not cluster:
            # End process
            return

        while True:
            try:
                namespace.run(k8s_manager, cluster)
            except ApiException as e:
                namespace.logger.error(
                    "Exception when calling CoreV1Api->list_event_for_all_namespaces: %s\n", e)
                time.sleep(log_sleep_interval)
            except Exception as e:
                namespace.logger.exception("Unhandled exception occurred: %s\n", e)
