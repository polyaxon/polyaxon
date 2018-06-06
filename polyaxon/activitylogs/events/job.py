import activitylogs

from event_manager.events import job

activitylogs.subscribe(job.JobStartedTriggeredEvent)
activitylogs.subscribe(job.JobSoppedTriggeredEvent)
activitylogs.subscribe(job.JobViewedEvent)
