import auditor

from event_manager.events import pipeline

auditor.subscribe(pipeline.PipelineCreatedEvent)
auditor.subscribe(pipeline.PipelineUpdatedEvent)
auditor.subscribe(pipeline.PipelineCleanedTriggeredEvent)
auditor.subscribe(pipeline.PipelineViewedEvent)
auditor.subscribe(pipeline.PipelineArchivedEvent)
auditor.subscribe(pipeline.PipelineRestoredEvent)
auditor.subscribe(pipeline.PipelineBookmarkedEvent)
auditor.subscribe(pipeline.PipelineUnbookmarkedEvent)
auditor.subscribe(pipeline.PipelineDeletedEvent)
auditor.subscribe(pipeline.PipelineDeletedTriggeredEvent)
