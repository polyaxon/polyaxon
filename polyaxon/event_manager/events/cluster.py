from event_manager.event import Attribute, Event

CLUSTER_CREATED = 'cluster.created'
CLUSTER_UPDATED = 'cluster.updated'
CLUSTER_NODE_CREATED = 'cluster.node.created'
CLUSTER_NODE_UPDATED = 'cluster.node.updated'
CLUSTER_NODE_DELETED = 'cluster.node.deleted'
CLUSTER_NODE_GPU = 'cluster.node.gpu'


class ClusterCreatedEvent(Event):
    event_type = CLUSTER_CREATED
    attributes = (
        Attribute('created_at', is_datetime=True),
        Attribute('namespace'),
        Attribute('environment'),
        Attribute('is_upgrade'),
        Attribute('use_provisioner'),
        Attribute('use_data_claim'),
        Attribute('use_outputs_claim'),
        Attribute('use_logs_claim'),
        Attribute('use_repos_claim'),
        Attribute('use_upload_claim'),
        Attribute('cli_version'),
        Attribute('cli_min_version'),
        Attribute('cli_latest_version'),
        Attribute('platform_min_version'),
        Attribute('platform_latest_version'),
        Attribute('chart_version'),
        Attribute('cpu', attr_type=float),
        Attribute('memory', attr_type=float),
        Attribute('gpu', attr_type=float),
        Attribute('api_version', attr_type=dict)
    )


class ClusterUpdatedEvent(Event):
    event_type = CLUSTER_UPDATED
    attributes = (
        Attribute('updated_at', is_datetime=True),
        Attribute('is_upgrade'),
        Attribute('cpu', attr_type=float),
        Attribute('memory', attr_type=float),
        Attribute('gpu', attr_type=float),
    )


class ClusterNodeCreatedEvent(Event):
    event_type = CLUSTER_NODE_CREATED
    attributes = (
        Attribute('id'),
        Attribute('created_at', is_datetime=True),
        Attribute('role'),
        Attribute('sequence', attr_type=int),
        Attribute('docker_version'),
        Attribute('kubelet_version'),
        Attribute('os_image'),
        Attribute('kernel_version'),
        Attribute('cpu', attr_type=float),
        Attribute('memory', attr_type=float),
        Attribute('n_gpu', attr_type=int),
    )


class ClusterNodeUpdatedEvent(Event):
    event_type = CLUSTER_NODE_UPDATED
    attributes = (
        Attribute('id'),
        Attribute('update_at', is_datetime=True),
        Attribute('role'),
        Attribute('sequence', attr_type=int),
        Attribute('docker_version'),
        Attribute('kubelet_version'),
        Attribute('os_image'),
        Attribute('kernel_version'),
        Attribute('cpu', attr_type=float),
        Attribute('memory', attr_type=float),
        Attribute('n_gpu', attr_type=int),
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
