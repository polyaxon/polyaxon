import auditor
from libs.event_manager import event_types
from libs.event_manager.event import Event


class ClusterCreatedEvent(Event):
    type = event_types.CLUSTER_CREATED


class ClusterUpdatedEvent(Event):
    type = event_types.CLUSTER_UPDATED


class ClusterNodeCreatedEvent(Event):
    type = event_types.CLUSTER_NODE_CREATED


class ClusterNodeUpdatedEvent(Event):
    type = event_types.CLUSTER_NODE_UPDATED


class ClusterNodeDeletedEvent(Event):
    type = event_types.CLUSTER_NODE_DELETED


class ClusterNodeGPU(Event):
    type = event_types.CLUSTER_NODE_GPU


auditor.register(ClusterCreatedEvent)
auditor.register(ClusterUpdatedEvent)
auditor.register(ClusterNodeCreatedEvent)
auditor.register(ClusterNodeUpdatedEvent)
auditor.register(ClusterNodeGPU)
