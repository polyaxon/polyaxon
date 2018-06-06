import auditor

from event_manager.events import job

auditor.subscribe(job.JobStartedEvent)
auditor.subscribe(job.JobStartedTriggeredEvent)
auditor.subscribe(job.JobSoppedEvent)
auditor.subscribe(job.JobSoppedTriggeredEvent)
auditor.subscribe(job.JobViewedEvent)
auditor.subscribe(job.JobNewStatusEvent)
auditor.subscribe(job.JobFailedEvent)
auditor.subscribe(job.JobSucceededEvent)
