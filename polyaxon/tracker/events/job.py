import tracker

from event_manager.events import job

tracker.subscribe(job.JobStartedEvent)
tracker.subscribe(job.JobStartedTriggeredEvent)
tracker.subscribe(job.JobSoppedEvent)
tracker.subscribe(job.JobSoppedTriggeredEvent)
tracker.subscribe(job.JobViewedEvent)
tracker.subscribe(job.JobNewStatusEvent)
tracker.subscribe(job.JobFailedEvent)
tracker.subscribe(job.JobSucceededEvent)
