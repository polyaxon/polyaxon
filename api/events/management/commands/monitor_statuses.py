# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import time

from django.conf import settings

from kubernetes.client.rest import ApiException

from polyaxon_k8s.manager import K8SManager

from libs.utils import to_bool
from events.management.commands._base_monitor import BaseMonitorCommand
from events.monitors import statuses


class Command(BaseMonitorCommand):
    help = 'Watch jobs statuses events.'

    def handle(self, *args, **options):
        log_sleep_interval = options['log_sleep_interval']
        persist = to_bool(options['persist'])
        self.stdout.write(
            "Started a new statuses monitor with, "
            "log sleep interval: `{}` and persist: `{}`".format(log_sleep_interval, persist),
            ending='\n')
        k8s_manager = K8SManager(namespace=settings.K8S_NAMESPACE, in_cluster=True)
        while True:
            try:
                role_label = settings.ROLE_LABELS_WORKER
                type_label = settings.TYPE_LABELS_EXPERIMENT
                label_selector = 'role={},type={}'.format(role_label, type_label)
                statuses.run(k8s_manager,
                             job_container_name=settings.JOB_CONTAINER_NAME,
                             experiment_type_label=type_label,
                             label_selector=label_selector,
                             persist=persist)
            except ApiException as e:
                statuses.logger.error(
                    "Exception when calling CoreV1Api->list_namespaced_pod: %s\n" % e)
                time.sleep(settings.LOG_SLEEP_INTERVAL)
            except Exception as e:
                statuses.logger.exception("Unhandled exception occurred %s\n" % e)
