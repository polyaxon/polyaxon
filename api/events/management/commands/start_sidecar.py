# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function


from django.conf import settings


from polyaxon_k8s.manager import K8SManager

from libs.utils import to_bool
from events.management.commands._base_monitor import BaseMonitorCommand
from events.monitors import sidecar


class Command(BaseMonitorCommand):
    help = 'Watch jobs logs with a sidecar.'

    def add_arguments(self, parser):
        parser.add_argument('pod_id')
        parser.add_argument('container_job_name')
        super(Command, self).add_arguments(parser)

    def handle(self, *args, **options):
        pod_id = options['pod_id']
        container_job_name = options['container_job_name']
        log_sleep_interval = options['log_sleep_interval']
        persist = to_bool(options['persist'])
        self.stdout.write(
            "Started a new jobs logs / sidecar monitor with, pod_id: `{}` container_job_name: `{}`"
            "log sleep interval: `{}` and persist: `{}`".format(pod_id,
                                                                container_job_name,
                                                                log_sleep_interval,
                                                                persist),
            ending='\n')
        k8s_manager = K8SManager(namespace=settings.K8S_NAMESPACE, in_cluster=True)
        sidecar.can_log(k8s_manager, pod_id, log_sleep_interval)
        sidecar.run(k8s_manager, pod_id, container_job_name, persist)
        sidecar.logger.debug('Finished logging')
