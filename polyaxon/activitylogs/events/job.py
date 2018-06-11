import activitylogs

from event_manager.events import job

activitylogs.subscribe(job.JobStartedTriggeredEvent)
activitylogs.subscribe(job.JobSoppedTriggeredEvent)
activitylogs.subscribe(job.JobDeletedTriggeredEvent)
activitylogs.subscribe(job.JobCreatedEvent)
activitylogs.subscribe(job.JobUpdatedEvent)
activitylogs.subscribe(job.JobViewedEvent)
