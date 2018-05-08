import auditor
from libs.event_manager.base_events import cluster

auditor.register(cluster.ClusterCreatedEvent)
auditor.register(cluster.ClusterUpdatedEvent)
auditor.register(cluster.ClusterNodeCreatedEvent)
auditor.register(cluster.ClusterNodeUpdatedEvent)
auditor.register(cluster.ClusterNodeGPU)
