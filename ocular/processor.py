from ocular.constants import container_statuses, pod_statuses, pod_conditions, event_types, pod_lifecycle


def get_pod_details(event_type, event):
    labels = event['metadata']['labels']
    node_name = event['spec']['node_name']
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
        pod_conditions = {c['type']: {
            'status': c['status'],
            'reason': c['reason'],
            'message': c.get('message')
        } for c in pod_conditions}

    return {
        'event_type': event_type,
        'labels': labels,
        'phase': pod_phase,
        'deletion_timestamp': str(deletion_timestamp) if deletion_timestamp else None,
        'pod_conditions': pod_conditions,
        'container_statuses': container_statuses_by_name,
        'node_name': node_name
    }


def get_container_status(pod_details, job_container_names):
    job_container_status = None
    for job_container_name in job_container_names:
        job_container_status = pod_details['container_statuses'].get(job_container_name)
        if job_container_status:
            break
    return job_container_status


def get_failed_status(job_container_status):
    if not job_container_status:
        return pod_statuses.FAILED, None

    job_container_status_terminated = job_container_status['state'][
        container_statuses.TERMINATED]

    if job_container_status_terminated['reason'] == 'Error':
        return pod_statuses.FAILED, 'exist-code({})-message({})'.format(
            job_container_status_terminated['exit_code'],
            job_container_status_terminated['message'])

    return pod_statuses.FAILED, job_container_status_terminated['reason']


def get_job_status(pod_details, job_container_names):  # pylint:disable=too-many-branches
    # For terminated pods that failed and successfully terminated pods
    if pod_details['phase'] == pod_lifecycle.FAILED:
        job_container_status = get_container_status(pod_details=pod_details,
                                                    job_container_names=job_container_names)
        return get_failed_status(job_container_status=job_container_status)

    if pod_details['phase'] == pod_lifecycle.SUCCEEDED:
        return pod_statuses.SUCCEEDED, None

    if pod_details['deletion_timestamp']:
        return pod_statuses.STOPPED, 'Deletion time: {}'.format(pod_details['deletion_timestamp'])

    if not pod_details['pod_conditions']:
        return pod_statuses.UNKNOWN, 'Unknown pod conditions'

    if pod_conditions.UNSCHEDULABLE in pod_details['pod_conditions']:
        return (pod_statuses.UNSCHEDULABLE,
                pod_details['pod_conditions'][pod_conditions.UNSCHEDULABLE]['reason'])

    pod_has_scheduled_cond = pod_conditions.SCHEDULED in pod_details['pod_conditions']
    pod_has_ready_cond = pod_conditions.READY in pod_details['pod_conditions']

    check_cond = (pod_has_scheduled_cond and
                  not pod_details['pod_conditions'][pod_conditions.SCHEDULED]['status'])
    pod_is_unschedulable = (
        pod_has_scheduled_cond and
        pod_details['pod_conditions'][pod_conditions.SCHEDULED]['reason'] == pod_conditions.UNSCHEDULABLE)
    if pod_is_unschedulable:
        return (pod_statuses.UNSCHEDULABLE,
                pod_details['pod_conditions'][pod_conditions.SCHEDULED]['message'])
    if check_cond:
        return pod_statuses.BUILDING, pod_details['pod_conditions'][pod_conditions.SCHEDULED]['reason']

    if pod_has_scheduled_cond and not pod_has_ready_cond:
        return pod_statuses.BUILDING, None

    job_container_status = get_container_status(pod_details=pod_details,
                                                job_container_names=job_container_names)

    if not job_container_status:
        return pod_statuses.UNKNOWN, None

    job_container_status_terminated = job_container_status['state'][container_statuses.TERMINATED]
    if job_container_status_terminated:
        if job_container_status_terminated['reason'] == 'Completed':
            return pod_statuses.SUCCEEDED, job_container_status_terminated['reason']
        return get_failed_status(job_container_status=job_container_status)

    job_container_status_waiting = job_container_status['state'][container_statuses.WAITING]
    if job_container_status_waiting:
        return pod_statuses.BUILDING, job_container_status_waiting['reason']
    job_container_status_running = job_container_status['state'][container_statuses.RUNNING]
    if job_container_status['state'][container_statuses.RUNNING]:
        return pod_statuses.RUNNING, job_container_status_running.get('reason')

    # Unknown?
    return pod_statuses.UNKNOWN, None


def get_pod_state(event_type, event, job_container_names, created_at):
    pod_details = get_pod_details(event_type=event_type, event=event)
    status, message = get_job_status(pod_details, job_container_names)
    pod_state = {
        'status': status,
        'message': message,
        'details': pod_details
    }
    if created_at:
        pod_state['created_at'] = created_at
    return pod_state
