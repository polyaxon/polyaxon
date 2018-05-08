from libs.event_manager.event import Event

EXPERIMENT_CREATED = 'experiment.created'
EXPERIMENT_UPDATED = 'experiment.updated'  # params same user, other user, access granted
EXPERIMENT_DELETED = 'experiment.deleted'  # params same user, other user, access granted
EXPERIMENT_VIEWED = 'experiment.viewed'  # params same user, other user, access granted
EXPERIMENT_STOPPED = 'experiment.stopped'  # params same user, other user, access granted
EXPERIMENT_RESUMED = 'experiment.resumed'  # params same user, other user, access granted
EXPERIMENT_RESTARTED = 'experiment.restarted'  # params same user, other user, access granted
EXPERIMENT_COPIED = 'experiment.copied'  # params same user, other user, access granted
EXPERIMENT_NEW_STATUS = 'experiment.new_status'
EXPERIMENT_SUCCEEDED = 'experiment.succeeded'
EXPERIMENT_FAILED = 'experiment.failed'
EXPERIMENT_RESOURCES_VIEWED = 'experiment.resources_viewed'  # params same user, other user, access granted
EXPERIMENT_LOGS_VIEWED = 'experiment.logs_viewed'  # params same user, other user, access granted
EXPERIMENT_STATUSES_VIEWED = 'experiment.statuses_viewed'
EXPERIMENT_JOBS_VIEWED = 'experiment.jobs_viewed'
EXPERIMENT_JOB_VIEWED = 'experiment.job.viewed'  # params same user, other user, access granted
EXPERIMENT_JOB_RESOURCES_VIEWED = 'experiment.job.resources_viewed'  # params same user, other user, access granted
EXPERIMENT_JOB_LOGS_VIEWED = 'experiment.job.logs_viewed'  # params same user, other user, access granted
EXPERIMENT_JOB_STATUSES_VIEWED = 'experiment.job.statuses_viewed'


class ExperimentCreatedEvent(Event):
    type = EXPERIMENT_CREATED


class ExperimentUpdatedEvent(Event):
    type = EXPERIMENT_UPDATED


class ExperimentDeletedEvent(Event):
    type = EXPERIMENT_DELETED


class ExperimentViewedEvent(Event):
    type = EXPERIMENT_VIEWED


class ExperimentStoppedEvent(Event):
    type = EXPERIMENT_STOPPED


class ExperimentResumedEvent(Event):
    type = EXPERIMENT_RESUMED


class ExperimentRestartedEvent(Event):
    type = EXPERIMENT_RESTARTED


class ExperimentCopiedEvent(Event):
    type = EXPERIMENT_COPIED


class ExperimentNewStatusEvent(Event):
    type = EXPERIMENT_NEW_STATUS


class ExperimentSucceededEvent(Event):
    type = EXPERIMENT_SUCCEEDED


class ExperimentFailedEvent(Event):
    type = EXPERIMENT_FAILED


class ExperimentResourcesViewedEvent(Event):
    type = EXPERIMENT_RESOURCES_VIEWED


class ExperimentLogsViewedEvent(Event):
    type = EXPERIMENT_LOGS_VIEWED


class ExperimentStatusesViewedEvent(Event):
    type = EXPERIMENT_STATUSES_VIEWED


class ExperimentJobsViewedEvent(Event):
    type = EXPERIMENT_JOBS_VIEWED


class ExperimentJobViewedEvent(Event):
    type = EXPERIMENT_JOB_VIEWED


class ExperimentJobResourcesViewedEvent(Event):
    type = EXPERIMENT_JOB_RESOURCES_VIEWED


class ExperimentJobLogsViewedEvent(Event):
    type = EXPERIMENT_JOB_LOGS_VIEWED


class ExperimentJobStatusesViewedEvent(Event):
    type = EXPERIMENT_JOB_STATUSES_VIEWED
