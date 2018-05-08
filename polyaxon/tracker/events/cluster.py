import tracker
from event_manager.events import cluster

tracker.subscribe(cluster.ClusterCreatedEvent)
tracker.subscribe(cluster.ClusterUpdatedEvent)
tracker.subscribe(cluster.ClusterNodeCreatedEvent)
tracker.subscribe(cluster.ClusterNodeUpdatedEvent)
tracker.subscribe(cluster.ClusterNodeDeletedEvent)
tracker.subscribe(cluster.ClusterNodeGPU)
