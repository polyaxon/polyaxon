import tracker

from event_manager.events import job

tracker.subscribe(job.JobCreatedEvent)
tracker.subscribe(job.JobUpdatedEvent)
tracker.subscribe(job.JobStartedEvent)
tracker.subscribe(job.JobStartedTriggeredEvent)
tracker.subscribe(job.JobSoppedEvent)
tracker.subscribe(job.JobSoppedTriggeredEvent)
tracker.subscribe(job.JobViewedEvent)
tracker.subscribe(job.JobNewStatusEvent)
tracker.subscribe(job.JobFailedEvent)
tracker.subscribe(job.JobSucceededEvent)
tracker.subscribe(job.JobDoneEvent)
tracker.subscribe(job.JobDeletedEvent)
tracker.subscribe(job.JobDeletedTriggeredEvent)
tracker.subscribe(job.JobLogsViewedEvent)
tracker.subscribe(job.JobRestartedEvent)
tracker.subscribe(job.JobRestartedTriggeredEvent)
tracker.subscribe(job.JobStatusesViewedEvent)
