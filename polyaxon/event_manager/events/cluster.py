from event_manager import event_actions, event_subjects
from event_manager.event import Attribute, Event

CLUSTER_CREATED = '{}.{}'.format(event_subjects.CLUSTER, event_actions.CREATED)
CLUSTER_UPDATED = '{}.{}'.format(event_subjects.CLUSTER, event_actions.UPDATED)
CLUSTER_RESOURCES_UPDATED = '{}.resources_updated'.format(event_subjects.CLUSTER)
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
        Attribute('provisioner_enabled', attr_type=bool),
        Attribute('node_selector_core_enabled', attr_type=bool),
        Attribute('node_selector_experiments_enabled', attr_type=bool),
        Attribute('cli_min_version'),
        Attribute('cli_latest_version'),
        Attribute('platform_min_version'),
        Attribute('platform_latest_version'),
        Attribute('chart_version'),
        Attribute('version_api', attr_type=dict)
    )


class ClusterUpdatedEvent(Event):
    event_type = CLUSTER_UPDATED
    attributes = (
        Attribute('updated_at', is_datetime=True),
        Attribute('is_upgrade', attr_type=bool),
        Attribute('version_api', attr_type=dict)
    )


class ClusterResourcesUpdatedEvent(Event):
    event_type = CLUSTER_RESOURCES_UPDATED
    attributes = (
        Attribute('updated_at', is_datetime=True),
        Attribute('n_nodes', attr_type=float),
        Attribute('n_cpus', attr_type=float),
        Attribute('memory', attr_type=float),
        Attribute('n_gpus', attr_type=float),
    )


class ClusterNodeCreatedEvent(Event):
    event_type = CLUSTER_NODE_CREATED
    attributes = (
        Attribute('id'),
        Attribute('role'),
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
        Attribute('role'),
        Attribute('docker_version', is_required=False),
        Attribute('kubelet_version'),
        Attribute('os_image'),
        Attribute('kernel_version'),
        Attribute('cpu', attr_type=float),
        Attribute('memory', attr_type=float),
        Attribute('n_gpus', attr_type=int),
    )


class ClusterNodeGPU(Event):
    event_type = CLUSTER_NODE_GPU
    attributes = (
        Attribute('created_at', is_datetime=True),
        Attribute('serial'),
        Attribute('name'),
        Attribute('memory', attr_type=int),
    )
