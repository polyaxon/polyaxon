import tracker

from event_manager.events import operation

tracker.subscribe(operation.OperationCreatedEvent)
tracker.subscribe(operation.OperationUpdatedEvent)
tracker.subscribe(operation.OperationCleanedTriggeredEvent)
tracker.subscribe(operation.OperationViewedEvent)
tracker.subscribe(operation.OperationArchivedEvent)
tracker.subscribe(operation.OperationRestoredEvent)
tracker.subscribe(operation.OperationDeletedEvent)
tracker.subscribe(operation.OperationDeletedTriggeredEvent)
