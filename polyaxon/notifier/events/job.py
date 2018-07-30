import notifier

from event_manager.events import job

notifier.subscribe_event(job.JobStartedEvent)
notifier.subscribe_event(job.JobSoppedEvent)
notifier.subscribe_event(job.JobNewStatusEvent)
notifier.subscribe_event(job.JobFailedEvent)
notifier.subscribe_event(job.JobSucceededEvent)
notifier.subscribe_event(job.JobDoneEvent)
notifier.subscribe_event(job.JobDeletedEvent)
