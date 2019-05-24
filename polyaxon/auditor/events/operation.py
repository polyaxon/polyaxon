import auditor

from events.registry import operation

auditor.subscribe(operation.OperationCreatedEvent)
auditor.subscribe(operation.OperationUpdatedEvent)
auditor.subscribe(operation.OperationCleanedTriggeredEvent)
auditor.subscribe(operation.OperationViewedEvent)
auditor.subscribe(operation.OperationArchivedEvent)
auditor.subscribe(operation.OperationRestoredEvent)
auditor.subscribe(operation.OperationDeletedEvent)
auditor.subscribe(operation.OperationDeletedTriggeredEvent)
