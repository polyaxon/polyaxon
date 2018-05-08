from event_manager.event import Attribute, Event

EXPERIMENT_CREATED = 'experiment.created'
EXPERIMENT_UPDATED = 'experiment.updated'
EXPERIMENT_DELETED = 'experiment.deleted'
EXPERIMENT_VIEWED = 'experiment.viewed'
EXPERIMENT_STOPPED = 'experiment.stopped'
EXPERIMENT_RESUMED = 'experiment.resumed'
EXPERIMENT_RESTARTED = 'experiment.restarted'
EXPERIMENT_COPIED = 'experiment.copied'
EXPERIMENT_NEW_STATUS = 'experiment.new_status'
EXPERIMENT_SUCCEEDED = 'experiment.succeeded'
EXPERIMENT_FAILED = 'experiment.failed'
EXPERIMENT_RESOURCES_VIEWED = 'experiment.resources_viewed'
EXPERIMENT_LOGS_VIEWED = 'experiment.logs_viewed'
EXPERIMENT_STATUSES_VIEWED = 'experiment.statuses_viewed'
EXPERIMENT_JOBS_VIEWED = 'experiment.jobs_viewed'
EXPERIMENT_JOB_VIEWED = 'experiment.job.viewed'
EXPERIMENT_JOB_RESOURCES_VIEWED = 'experiment.job.resources_viewed'
EXPERIMENT_JOB_LOGS_VIEWED = 'experiment.job.logs_viewed'
EXPERIMENT_JOB_STATUSES_VIEWED = 'experiment.job.statuses_viewed'


class ExperimentCreatedEvent(Event):
    type = EXPERIMENT_CREATED
    attributes = (
        Attribute('id'),
        Attribute('project.id'),
        Attribute('project.user.id'),
        Attribute('experiment_group.id'),
        Attribute('experiment_group.user.id'),
        Attribute('user.id'),
        Attribute('created_at', is_datetime=True),
        Attribute('has_description', attr_type=bool),
        Attribute('is_resume', attr_type=bool),
        Attribute('is_restart', attr_type=bool),
        Attribute('is_copy', attr_type=bool),
    )


class ExperimentUpdatedEvent(Event):
    type = EXPERIMENT_UPDATED
    attributes = (
        Attribute('id'),
        Attribute('sequence'),
        Attribute('project.id'),
        Attribute('project.user.id'),
        Attribute('experiment_group.id'),
        Attribute('experiment_group.user.id'),
        Attribute('user.id'),
        Attribute('actor_id'),
        Attribute('update_at', is_datetime=True),
        Attribute('has_description', attr_type=bool),
        Attribute('status'),
    )


class ExperimentDeletedEvent(Event):
    type = EXPERIMENT_DELETED
    attributes = (
        Attribute('id'),
        Attribute('sequence'),
        Attribute('project.id'),
        Attribute('project.user.id'),
        Attribute('experiment_group.id'),
        Attribute('experiment_group.user.id'),
        Attribute('user.id'),
        Attribute('actor_id'),
        Attribute('updated_at', is_datetime=True),
        Attribute('has_description', attr_type=bool),
        Attribute('status'),
    )


class ExperimentViewedEvent(Event):
    type = EXPERIMENT_VIEWED
    attributes = (
        Attribute('id'),
        Attribute('sequence'),
        Attribute('project.id'),
        Attribute('project.user.id'),
        Attribute('experiment_group.id'),
        Attribute('experiment_group.user.id'),
        Attribute('user.id'),
        Attribute('actor_id'),
        Attribute('has_description', attr_type=bool),
        Attribute('status'),
    )


class ExperimentStoppedEvent(Event):
    type = EXPERIMENT_STOPPED
    attributes = (
        Attribute('id'),
        Attribute('sequence'),
        Attribute('project.id'),
        Attribute('project.user.id'),
        Attribute('experiment_group.id'),
        Attribute('experiment_group.user.id'),
        Attribute('user.id'),
        Attribute('actor_id'),
        Attribute('has_description', attr_type=bool),
        Attribute('status'),
    )


class ExperimentResumedEvent(Event):
    type = EXPERIMENT_RESUMED
    attributes = (
        Attribute('id'),
        Attribute('sequence'),
        Attribute('project.id'),
        Attribute('project.user.id'),
        Attribute('experiment_group.id'),
        Attribute('experiment_group.user.id'),
        Attribute('user.id'),
        Attribute('actor_id'),
        Attribute('has_description', attr_type=bool),
        Attribute('status'),
    )


class ExperimentRestartedEvent(Event):
    type = EXPERIMENT_RESTARTED
    attributes = (
        Attribute('id'),
        Attribute('sequence'),
        Attribute('project.id'),
        Attribute('project.user.id'),
        Attribute('experiment_group.id'),
        Attribute('experiment_group.user.id'),
        Attribute('user.id'),
        Attribute('actor_id'),
        Attribute('has_description', attr_type=bool),
        Attribute('status'),
    )


class ExperimentCopiedEvent(Event):
    type = EXPERIMENT_COPIED
    attributes = (
        Attribute('id'),
        Attribute('sequence'),
        Attribute('project.id'),
        Attribute('project.user.id'),
        Attribute('experiment_group.id'),
        Attribute('experiment_group.user.id'),
        Attribute('user.id'),
        Attribute('actor_id'),
        Attribute('has_description', attr_type=bool),
        Attribute('status'),
    )


class ExperimentNewStatusEvent(Event):
    type = EXPERIMENT_NEW_STATUS
    attributes = (
        Attribute('id'),
        Attribute('sequence'),
        Attribute('project.id'),
        Attribute('experiment_group.id'),
        Attribute('status'),
    )


class ExperimentSucceededEvent(Event):
    type = EXPERIMENT_SUCCEEDED
    attributes = (
        Attribute('id'),
        Attribute('sequence'),
        Attribute('project.id'),
        Attribute('experiment_group.id'),
    )


class ExperimentFailedEvent(Event):
    type = EXPERIMENT_FAILED
    attributes = (
        Attribute('id'),
        Attribute('sequence'),
        Attribute('project.id'),
        Attribute('experiment_group.id'),
    )


class ExperimentResourcesViewedEvent(Event):
    type = EXPERIMENT_RESOURCES_VIEWED
    attributes = (
        Attribute('id'),
        Attribute('sequence'),
        Attribute('project.id'),
        Attribute('project.user.id'),
        Attribute('experiment_group.id'),
        Attribute('experiment_group.user.id'),
        Attribute('user.id'),
        Attribute('actor_id'),
        Attribute('status'),
    )


class ExperimentLogsViewedEvent(Event):
    type = EXPERIMENT_LOGS_VIEWED
    attributes = (
        Attribute('id'),
        Attribute('sequence'),
        Attribute('project.id'),
        Attribute('project.user.id'),
        Attribute('experiment_group.id'),
        Attribute('experiment_group.user.id'),
        Attribute('user.id'),
        Attribute('actor_id'),
        Attribute('status'),
    )


class ExperimentStatusesViewedEvent(Event):
    type = EXPERIMENT_STATUSES_VIEWED
    attributes = (
        Attribute('id'),
        Attribute('sequence'),
        Attribute('project.id'),
        Attribute('project.user.id'),
        Attribute('experiment_group.id'),
        Attribute('experiment_group.user.id'),
        Attribute('user.id'),
        Attribute('actor_id'),
        Attribute('status'),
    )


class ExperimentJobsViewedEvent(Event):
    type = EXPERIMENT_JOBS_VIEWED
    attributes = (
        Attribute('id'),
        Attribute('sequence'),
        Attribute('project.id'),
        Attribute('project.user.id'),
        Attribute('experiment_group.id'),
        Attribute('experiment_group.user.id'),
        Attribute('user.id'),
        Attribute('actor_id'),
        Attribute('status'),
    )


class ExperimentJobViewedEvent(Event):
    type = EXPERIMENT_JOB_VIEWED
    attributes = (
        Attribute('id'),
        Attribute('sequence'),
        Attribute('role'),
        Attribute('experiment.id'),
        Attribute('experiment.user.id'),
        Attribute('actor_id'),
        Attribute('status'),
    )


class ExperimentJobResourcesViewedEvent(Event):
    type = EXPERIMENT_JOB_RESOURCES_VIEWED
    attributes = (
        Attribute('id'),
        Attribute('sequence'),
        Attribute('experiment.id'),
        Attribute('experiment.user.id'),
        Attribute('actor_id'),
        Attribute('status'),
    )


class ExperimentJobLogsViewedEvent(Event):
    type = EXPERIMENT_JOB_LOGS_VIEWED
    attributes = (
        Attribute('id'),
        Attribute('sequence'),
        Attribute('experiment.id'),
        Attribute('experiment.user.id'),
        Attribute('actor_id'),
        Attribute('status'),
    )


class ExperimentJobStatusesViewedEvent(Event):
    type = EXPERIMENT_JOB_STATUSES_VIEWED
    attributes = (
        Attribute('id'),
        Attribute('sequence'),
        Attribute('experiment.id'),
        Attribute('experiment.user.id'),
        Attribute('actor_id'),
        Attribute('status'),
    )
