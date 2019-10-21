import tracker

from events.registry import cluster

tracker.subscribe(cluster.ClusterCreatedEvent)
tracker.subscribe(cluster.ClusterUpdatedEvent)
tracker.subscribe(cluster.ClusterResourcesUpdatedEvent)
tracker.subscribe(cluster.ClusterNodeCreatedEvent)
tracker.subscribe(cluster.ClusterNodeUpdatedEvent)
tracker.subscribe(cluster.ClusterNodeDeletedEvent)
tracker.subscribe(cluster.ClusterNodeGPU)
