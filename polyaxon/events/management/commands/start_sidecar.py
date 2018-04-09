from django.conf import settings

from events.management.commands._base_monitor import BaseMonitorCommand
from events.monitors import sidecar
from polyaxon_k8s.manager import K8SManager


class Command(BaseMonitorCommand):
    help = 'Watch jobs logs with a sidecar.'

    def add_arguments(self, parser):
        parser.add_argument('pod_id')
        super(Command, self).add_arguments(parser)

    def handle(self, *args, **options):
        pod_id = options['pod_id']
        log_sleep_interval = options['log_sleep_interval']
        self.stdout.write(
            "Started a new jobs logs / sidecar monitor with, pod_id: `{}` container_job_name: `{}`"
            "log sleep interval: `{}`".format(pod_id,
                                              settings.CONTAINER_NAME_JOB,
                                              log_sleep_interval),
            ending='\n')
        k8s_manager = K8SManager(namespace=settings.K8S_NAMESPACE, in_cluster=True)
        is_running, labels = sidecar.can_log(k8s_manager, pod_id, log_sleep_interval)
        if not is_running:
            sidecar.logger.info('Jobs is not running anymore.')
            return 

        sidecar.run(k8s_manager=k8s_manager,
                    pod_id=pod_id,
                    experiment_uuid=labels.experiment_uuid.hex,
                    experiment_name=labels.experiment_name,
                    job_uuid=labels.job_uuid.hex,
                    task_type=labels.task_type,
                    task_idx=labels.task_idx,
                    container_job_name=settings.CONTAINER_NAME_JOB)
        sidecar.logger.info('Finished logging')
