# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function


def get_pod_state(raw_event):
    event_type = raw_event['type']
    event = raw_event['object']
    labels = event.metadata.labels
    pod_phase = event.status.phase
    deletion_timestamp = event.metadata.deletion_timestamp
    pod_conditions = event.status.conditions
    container_statuses = event.status.container_statuses
    container_statuses_by_name = {}
    if container_statuses:
        container_statuses_by_name = {
            container_status.name: {
                'ready': container_status.ready,
                'state': container_status.state.to_dict(),
            } for container_status in container_statuses
        }

    if pod_conditions:
        pod_conditions = {c.type: {'status': c.status, 'reason': c.reason} for c in pod_conditions}

    return {
        'event_type': event_type,
        'labels': labels,
        'phase': pod_phase,
        'deletion_timestamp': deletion_timestamp,
        'pod_conditions': pod_conditions,
        'container_statuses': container_statuses_by_name
    }
