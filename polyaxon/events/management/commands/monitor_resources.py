import time

from django.conf import settings
from django.db import ProgrammingError

from clusters.models import Cluster
from events.management.commands._base_monitor import BaseMonitorCommand
from events.monitors import resources
from libs.utils import to_bool
from runner.nodes.models import ClusterNode


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
        while True:
            try:
                return self.get_node()
            except ProgrammingError:
                time.sleep(log_sleep_interval * 2)

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
                resources.run(containers, node, persist)
            except Exception as e:
                resources.logger.exception("Unhandled exception occurred %s\n", e)

            time.sleep(log_sleep_interval)
            if node:
                node.refresh_from_db()
            else:
                node = self.get_node()
