# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function


import time

from django.conf import settings

from kubernetes.client.rest import ApiException

from polyaxon_k8s.manager import K8SManager

from clusters.utils import get_cluster

from libs.utils import to_bool
from events.management.commands._base_monitor import BaseMonitorCommand
from events.monitors import namespace


class Command(BaseMonitorCommand):
    help = 'Watch namespace warning and errors events.'

    def handle(self, *args, **options):
        log_sleep_interval = options['log_sleep_interval']
        persist = to_bool(options['persist'])
        self.stdout.write(
            "Started a new namespace monitor with, "
            "log sleep interval: `{}` and persist: `{}`".format(log_sleep_interval, persist),
            ending='\n')
        k8s_manager = K8SManager(namespace=settings.K8S_NAMESPACE, in_cluster=True)
        cluster = get_cluster()
        while True:
            try:
                namespace.run(k8s_manager, cluster, persist)
            except ApiException as e:
                namespace.logger.error(
                    "Exception when calling CoreV1Api->list_event_for_all_namespaces: %s\n" % e)
                time.sleep(log_sleep_interval)
            except Exception as e:
                namespace.logger.exception("Unhandled exception occurred: %s\n" % e)
