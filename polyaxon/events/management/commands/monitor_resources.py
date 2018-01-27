# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import time

from django.conf import settings

from clusters.models import ClusterNode, Cluster
from libs.utils import to_bool
from events.management.commands._base_monitor import BaseMonitorCommand
from events.monitors import resources


class Command(BaseMonitorCommand):
    help = 'Watch jobs/containers resources.'

    @staticmethod
    def get_node():
        cluster = Cluster.load()
        node = ClusterNode.objects.filter(cluster=cluster, name=settings.K8S_NODE_NAME)
        if node.count():
            return node.first()
        return None

    def handle(self, *args, **options):
        log_sleep_interval = options['log_sleep_interval']
        persist = to_bool(options['persist'])
        node = self.get_node()
        self.stdout.write(
            "Started a new resources monitor with, "
            "log sleep interval: `{}` and persist: `{}`".format(log_sleep_interval, persist),
            ending='\n')
        containers = {}
        while True:
            try:
                resources.run(containers, node, persist)
            except Exception as e:
                resources.logger.exception("Unhandled exception occurred %s\n" % e)

            time.sleep(log_sleep_interval)
            if node:
                node.refresh_from_db()
            else:
                node = self.get_node()
