import notifier

from events.registry import build_job

# notifier.subscribe_event(build_job.BuildJobStartedEvent)
# notifier.subscribe_event(build_job.BuildJobNewStatusEvent)
# notifier.subscribe_event(build_job.BuildJobDoneEvent)
notifier.subscribe_event(build_job.BuildJobSoppedEvent)
notifier.subscribe_event(build_job.BuildJobFailedEvent)
notifier.subscribe_event(build_job.BuildJobSucceededEvent)
