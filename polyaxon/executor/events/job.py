import executor

from event_manager.events import job

executor.subscribe(job.JobCreatedEvent)
executor.subscribe(job.JobStartedEvent)
executor.subscribe(job.JobSoppedEvent)
executor.subscribe(job.JobCleanedTriggeredEvent)
executor.subscribe(job.JobNewStatusEvent)
executor.subscribe(job.JobFailedEvent)
executor.subscribe(job.JobSucceededEvent)
executor.subscribe(job.JobDoneEvent)
executor.subscribe(job.JobDeletedEvent)
executor.subscribe(job.JobRestartedEvent)
