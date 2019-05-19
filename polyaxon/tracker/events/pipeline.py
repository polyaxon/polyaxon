import tracker

from event_manager.events import pipeline

tracker.subscribe(pipeline.PipelineCreatedEvent)
tracker.subscribe(pipeline.PipelineUpdatedEvent)
tracker.subscribe(pipeline.PipelineCleanedTriggeredEvent)
tracker.subscribe(pipeline.PipelineViewedEvent)
tracker.subscribe(pipeline.PipelineArchivedEvent)
tracker.subscribe(pipeline.PipelineRestoredEvent)
tracker.subscribe(pipeline.PipelineBookmarkedEvent)
tracker.subscribe(pipeline.PipelineUnbookmarkedEvent)
tracker.subscribe(pipeline.PipelineDeletedEvent)
tracker.subscribe(pipeline.PipelineDeletedTriggeredEvent)
