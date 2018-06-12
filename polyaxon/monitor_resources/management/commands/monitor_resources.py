import time

from django.conf import settings
from django.db import InterfaceError, OperationalError, ProgrammingError

from db.models.clusters import Cluster
from db.models.nodes import ClusterNode
from libs.base_monitor import BaseMonitorCommand
from libs.utils import to_bool
from monitor_resources import monitor


class Command(BaseMonitorCommand):
    help = 'Watch jobs/containers resources.'

    @staticmethod
    def get_node():
        cluster = Cluster.load()
        node = ClusterNode.objects.filter(cluster=cluster, name=settings.K8S_NODE_NAME)
        if node.count():
            return node.first()
        return None

    def get_node_or_wait(self, log_sleep_interval):
        max_trials = 10
        trials = 0
        while trials < max_trials:
            try:
                return self.get_node()
            except (InterfaceError, ProgrammingError, OperationalError) as e:
                monitor._logger.exception("Database is not synced yet %s\n", e)
                trials += 1
                time.sleep(log_sleep_interval * 2)
        return None

    def handle(self, *args, **options):
        log_sleep_interval = options['log_sleep_interval']
        persist = to_bool(options['persist'])
        node = self.get_node_or_wait(log_sleep_interval)
        self.stdout.write(
            "Started a new resources monitor with, "
            "log sleep interval: `{}` and persist: `{}`".format(log_sleep_interval, persist),
            ending='\n')
        containers = {}
        while True:
            try:
                if node:
                    monitor.run(containers, node, persist)
            except Exception as e:
                monitor.logger.exception("Unhandled exception occurred %s\n", e)

            time.sleep(log_sleep_interval)
            try:
                if node:
                    node.refresh_from_db()
                else:
                    node = self.get_node()
            except (InterfaceError, ProgrammingError, OperationalError) as e:
                monitor.logger.exception("Database connection is probably already closed %s\n", e)
                return
