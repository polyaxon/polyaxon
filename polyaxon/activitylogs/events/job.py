import activitylogs

from event_manager.events import job

activitylogs.subscribe(job.JobStartedTriggeredEvent)
activitylogs.subscribe(job.JobSoppedTriggeredEvent)
activitylogs.subscribe(job.JobDeletedTriggeredEvent)
activitylogs.subscribe(job.JobCreatedEvent)
activitylogs.subscribe(job.JobUpdatedEvent)
activitylogs.subscribe(job.JobViewedEvent)
activitylogs.subscribe(job.JobArchivedEvent)
activitylogs.subscribe(job.JobRestoredEvent)
activitylogs.subscribe(job.JobBookmarkedEvent)
activitylogs.subscribe(job.JobUnBookmarkedEvent)
activitylogs.subscribe(job.JobLogsViewedEvent)
activitylogs.subscribe(job.JobRestartedTriggeredEvent)
activitylogs.subscribe(job.JobStatusesViewedEvent)
activitylogs.subscribe(job.JobOutputsDownloadedEvent)
