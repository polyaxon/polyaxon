import auditor
from event_manager.events import cluster

auditor.subscribe(cluster.ClusterCreatedEvent)
auditor.subscribe(cluster.ClusterUpdatedEvent)
auditor.subscribe(cluster.ClusterNodeCreatedEvent)
auditor.subscribe(cluster.ClusterNodeUpdatedEvent)
auditor.subscribe(cluster.ClusterNodeGPU)
