# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from polyaxon_schemas.experiment import PodStateConfig


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
