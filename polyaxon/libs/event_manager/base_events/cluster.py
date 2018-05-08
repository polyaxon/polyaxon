from libs.event_manager.event import Event

CLUSTER_CREATED = 'cluster.created'
CLUSTER_UPDATED = 'cluster.updated'
CLUSTER_NODE_CREATED = 'cluster.node.created'
CLUSTER_NODE_UPDATED = 'cluster.node.updated'
CLUSTER_NODE_DELETED = 'cluster.node.deleted'
CLUSTER_NODE_GPU = 'cluster.node.gpu'


class ClusterCreatedEvent(Event):
    type = CLUSTER_CREATED


class ClusterUpdatedEvent(Event):
    type = CLUSTER_UPDATED


class ClusterNodeCreatedEvent(Event):
    type = CLUSTER_NODE_CREATED


class ClusterNodeUpdatedEvent(Event):
    type = CLUSTER_NODE_UPDATED


class ClusterNodeDeletedEvent(Event):
    type = CLUSTER_NODE_DELETED


class ClusterNodeGPU(Event):
    type = CLUSTER_NODE_GPU
