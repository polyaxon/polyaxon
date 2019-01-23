import executor

from event_manager.events import build_job

executor.subscribe(build_job.BuildJobCreatedEvent)
executor.subscribe(build_job.BuildJobSoppedEvent)
executor.subscribe(build_job.BuildJobCleanedTriggeredEvent)
executor.subscribe(build_job.BuildJobNewStatusEvent)
executor.subscribe(build_job.BuildJobFailedEvent)
executor.subscribe(build_job.BuildJobSucceededEvent)
executor.subscribe(build_job.BuildJobDoneEvent)
