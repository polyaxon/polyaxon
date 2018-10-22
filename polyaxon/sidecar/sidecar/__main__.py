import argparse

from polyaxon_k8s.manager import K8SManager
from sidecar import monitor, settings
from sidecar.commands import start_experiment_sidecar, start_job_side_car

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--pod_id',
        type=str
    )
    parser.add_argument(
        '--kind',
        type=str
    )
    parser.add_argument(
        '--log_sleep_interval',
        default=2,
        type=int
    )
    args = parser.parse_args()
    arguments = args.__dict__

    pod_id = arguments.pop('pod_id')
    kind = arguments.pop('kind')
    log_sleep_interval = arguments.pop('log_sleep_interval')

    k8s_manager = K8SManager(namespace=settings.K8S_NAMESPACE, in_cluster=True)
    is_running, labels = monitor.can_log(k8s_manager, pod_id, log_sleep_interval)

    if not is_running:
        monitor.logger.info('Pod is not running anymore.')
    else:
        if kind == 'experiment':
            start_experiment_sidecar(monitor=monitor,
                                     k8s_manager=k8s_manager,
                                     pod_id=pod_id,
                                     labels=labels)
        elif kind == 'job':
            start_job_side_car(monitor=monitor,
                               k8s_manager=k8s_manager,
                               pod_id=pod_id,
                               labels=labels)
        else:
            monitor.logger.error('Pod kind is not recognized.')
    monitor.logger.info('Finished logging')
