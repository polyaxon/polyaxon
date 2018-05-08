import analytics
from libs.event_manager.base_events import cluster

analytics.register(cluster.ClusterCreatedEvent)
analytics.register(cluster.ClusterUpdatedEvent)
analytics.register(cluster.ClusterNodeCreatedEvent)
analytics.register(cluster.ClusterNodeUpdatedEvent)
analytics.register(cluster.ClusterNodeGPU)
