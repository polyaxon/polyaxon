import analytics
from libs.event_manager.base_events import cluster
from libs.event_manager.event import Attribute


class ClusterCreatedEvent(cluster.ClusterCreatedEvent):
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


class ClusterUpdatedEvent(cluster.ClusterUpdatedEvent):
    attributes = (
        Attribute('updated_at', is_datetime=True),
        Attribute('is_upgrade'),
        Attribute('cpu', attr_type=float),
        Attribute('memory', attr_type=float),
        Attribute('gpu', attr_type=float),
    )


class ClusterNodeCreatedEvent(cluster.ClusterNodeCreatedEvent):
    attributes = (
        Attribute('node_uuid'),
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


class ClusterNodeUpdatedEvent(cluster.ClusterNodeUpdatedEvent):
    attributes = (
        Attribute('node_uuid'),
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


class ClusterNodeDeletedEvent(cluster.ClusterNodeDeletedEvent):
    attributes = (
        Attribute('node_uuid'),
    )


analytics.register(ClusterCreatedEvent)
analytics.register(ClusterUpdatedEvent)
analytics.register(ClusterNodeCreatedEvent)
analytics.register(ClusterNodeUpdatedEvent)
analytics.register(cluster.ClusterNodeGPU)
