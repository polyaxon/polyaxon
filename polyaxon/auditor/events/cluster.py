import auditor
from event_manager.events import cluster

auditor.register(cluster.ClusterCreatedEvent)
auditor.register(cluster.ClusterUpdatedEvent)
auditor.register(cluster.ClusterNodeCreatedEvent)
auditor.register(cluster.ClusterNodeUpdatedEvent)
auditor.register(cluster.ClusterNodeGPU)
