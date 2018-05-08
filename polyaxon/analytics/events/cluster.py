import analytics
from event_manager.events import cluster

analytics.subscribe(cluster.ClusterCreatedEvent)
analytics.subscribe(cluster.ClusterUpdatedEvent)
analytics.subscribe(cluster.ClusterNodeCreatedEvent)
analytics.subscribe(cluster.ClusterNodeUpdatedEvent)
analytics.subscribe(cluster.ClusterNodeGPU)
