import analytics
from event_manager.events import cluster

analytics.register(cluster.ClusterCreatedEvent)
analytics.register(cluster.ClusterUpdatedEvent)
analytics.register(cluster.ClusterNodeCreatedEvent)
analytics.register(cluster.ClusterNodeUpdatedEvent)
analytics.register(cluster.ClusterNodeGPU)
