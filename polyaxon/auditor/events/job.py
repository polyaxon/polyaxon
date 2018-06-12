import auditor

from event_manager.events import job

auditor.subscribe(job.JobCreatedEvent)
auditor.subscribe(job.JobUpdatedEvent)
auditor.subscribe(job.JobStartedEvent)
auditor.subscribe(job.JobStartedTriggeredEvent)
auditor.subscribe(job.JobSoppedEvent)
auditor.subscribe(job.JobSoppedTriggeredEvent)
auditor.subscribe(job.JobViewedEvent)
auditor.subscribe(job.JobNewStatusEvent)
auditor.subscribe(job.JobFailedEvent)
auditor.subscribe(job.JobSucceededEvent)
auditor.subscribe(job.JobDeletedEvent)
auditor.subscribe(job.JobDeletedTriggeredEvent)
auditor.subscribe(job.JobLogsViewedEvent)
auditor.subscribe(job.JobRestartedEvent)
auditor.subscribe(job.JobRestartedTriggeredEvent)
auditor.subscribe(job.JobStatusesViewedEvent)
