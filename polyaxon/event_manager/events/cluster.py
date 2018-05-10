from event_manager import event_actions, event_subjects
from event_manager.event import Attribute, Event

CLUSTER_CREATED = '{}.{}'.format(event_subjects.CLUSTER, event_actions.CREATED)
CLUSTER_UPDATED = '{}.{}'.format(event_subjects.CLUSTER, event_actions.UPDATED)
CLUSTER_NODE_CREATED = '{}.{}'.format(event_subjects.CLUSTER_NODE, event_actions.CREATED)
CLUSTER_NODE_UPDATED = '{}.{}'.format(event_subjects.CLUSTER_NODE, event_actions.UPDATED)
CLUSTER_NODE_DELETED = '{}.{}'.format(event_subjects.CLUSTER_NODE, event_actions.DELETED)
CLUSTER_NODE_GPU = '{}.gpu'.format(event_subjects.CLUSTER_NODE)


class ClusterCreatedEvent(Event):
    event_type = CLUSTER_CREATED
    attributes = (
        Attribute('created_at', is_datetime=True),
        Attribute('namespace'),
        Attribute('environment'),
        Attribute('is_upgrade'),
        Attribute('use_provisioner', attr_type=bool),
        Attribute('use_data_claim', attr_type=bool),
        Attribute('use_outputs_claim', attr_type=bool),
        Attribute('use_logs_claim', attr_type=bool),
        Attribute('use_repos_claim', attr_type=bool),
        Attribute('use_upload_claim', attr_type=bool),
        Attribute('cli_version'),
        Attribute('cli_min_version'),
        Attribute('cli_latest_version'),
        Attribute('platform_min_version'),
        Attribute('platform_latest_version'),
        Attribute('chart_version'),
        Attribute('cpu', attr_type=float),
        Attribute('memory', attr_type=float),
        Attribute('gpu', attr_type=float),
        Attribute('version_api', attr_type=dict)
    )


class ClusterUpdatedEvent(Event):
    event_type = CLUSTER_UPDATED
    attributes = (
        Attribute('updated_at', is_datetime=True),
        Attribute('is_upgrade', attr_type=bool),
        Attribute('cpu', attr_type=float),
        Attribute('memory', attr_type=float),
        Attribute('gpu', attr_type=float),
    )


class ClusterNodeCreatedEvent(Event):
    event_type = CLUSTER_NODE_CREATED
    attributes = (
        Attribute('id'),
        Attribute('role'),
        Attribute('sequence', attr_type=int),
        Attribute('docker_version', is_required=False),
        Attribute('kubelet_version'),
        Attribute('os_image'),
        Attribute('kernel_version'),
        Attribute('cpu', attr_type=float),
        Attribute('memory', attr_type=float),
        Attribute('n_gpus', attr_type=int),
    )


class ClusterNodeUpdatedEvent(Event):
    event_type = CLUSTER_NODE_UPDATED
    attributes = (
        Attribute('id'),
        Attribute('role'),
        Attribute('sequence', attr_type=int),
        Attribute('docker_version', is_required=False),
        Attribute('kubelet_version'),
        Attribute('os_image'),
        Attribute('kernel_version'),
        Attribute('cpu', attr_type=float),
        Attribute('memory', attr_type=float),
        Attribute('n_gpus', attr_type=int),
    )


class ClusterNodeDeletedEvent(Event):
    event_type = CLUSTER_NODE_DELETED
    attributes = (
        Attribute('id'),
    )


class ClusterNodeGPU(Event):
    event_type = CLUSTER_NODE_GPU
    attributes = (
        Attribute('created_at', is_datetime=True),
        Attribute('serial'),
        Attribute('name'),
        Attribute('memory', attr_type=int),
    )
