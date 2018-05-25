from constants.containers import ContainerStatuses
from constants.jobs import JobLifeCycle
from constants.pods import PodConditions, PodLifeCycle
from polyaxon_schemas.experiment import JobStateConfig, PodStateConfig


def get_pod_state(event_type, event):
    labels = event['metadata']['labels']
    pod_phase = event['status']['phase']
    deletion_timestamp = event['metadata']['deletion_timestamp']
    pod_conditions = event['status']['conditions']
    container_statuses = event['status']['container_statuses']
    container_statuses_by_name = {}
    if container_statuses:
        container_statuses_by_name = {
            container_status['name']: {
                'ready': container_status['ready'],
                'state': container_status['state'],
            } for container_status in container_statuses
        }

    if pod_conditions:
        pod_conditions = {c['type']: {'status': c['status'], 'reason': c['reason']}
                          for c in pod_conditions}

    return PodStateConfig.from_dict({
        'event_type': event_type,
        'labels': labels,
        'phase': pod_phase,
        'deletion_timestamp': str(deletion_timestamp) if deletion_timestamp else None,
        'pod_conditions': pod_conditions,
        'container_statuses': container_statuses_by_name
    })


def get_job_status(pod_state, job_container_names):
    # For terminated pods that failed and successfully terminated pods
    if pod_state.phase == PodLifeCycle.FAILED:
        return JobLifeCycle.FAILED, None

    if pod_state.phase == PodLifeCycle.SUCCEEDED:
        return JobLifeCycle.SUCCEEDED, None

    if pod_state.deletion_timestamp:
        return JobLifeCycle.STOPPED, 'Deletion time: {}'.format(pod_state.deletion_timestamp)

    if not pod_state.pod_conditions:
        return JobLifeCycle.UNKNOWN, 'Unknown pod conditions'

    if not pod_state.pod_conditions[PodConditions.SCHEDULED]['status']:
        return JobLifeCycle.BUILDING, pod_state['pod_conditions'][PodConditions.SCHEDULED]['reason']

    if not (pod_state.pod_conditions[PodConditions.SCHEDULED] or
            pod_state['pod_conditions'][PodConditions.READY]):
        return JobLifeCycle.BUILDING, PodConditions.READY

    if PodConditions.READY not in pod_state.pod_conditions:
        return JobLifeCycle.BUILDING, None

    job_container_status = None
    for job_container_name in job_container_names:
        job_container_status = pod_state.container_statuses.get(job_container_name)
        if job_container_status:
            break

    if not job_container_status:
        return PodLifeCycle.UNKNOWN, None

    job_container_status_terminated = job_container_status['state'][ContainerStatuses.TERMINATED]
    if job_container_status_terminated:
        if job_container_status_terminated['reason'] == 'Completed':
            return JobLifeCycle.SUCCEEDED, job_container_status_terminated['reason']
        if job_container_status_terminated['reason'] == 'Error':
            return JobLifeCycle.FAILED, 'exist-code({})-message({})'.format(
                job_container_status_terminated['exit_code'],
                job_container_status_terminated['message'])

    job_container_status_waiting = job_container_status['state'][ContainerStatuses.WAITING]
    if job_container_status_waiting:
        return JobLifeCycle.BUILDING, job_container_status_waiting['reason']
    job_container_status_running = job_container_status['state'][ContainerStatuses.RUNNING]
    if job_container_status['state'][ContainerStatuses.RUNNING]:
        return JobLifeCycle.RUNNING, job_container_status_running.get('reason')

    # Unknown?
    return PodLifeCycle.UNKNOWN, None


def get_job_state(event_type, event, job_container_names, experiment_type_label):
    pod_state = get_pod_state(event_type=event_type, event=event)
    if pod_state.labels.type != experiment_type_label:  # 2 types: core and experiment
        return

    status, message = get_job_status(pod_state, job_container_names)
    return JobStateConfig(
        status=status,
        message=message,
        details=pod_state,
    )
