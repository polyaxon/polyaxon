from event_manager.event import Attribute, Event

EXPERIMENT_JOB_VIEWED = 'experiment_job.viewed'
EXPERIMENT_JOB_RESOURCES_VIEWED = 'experiment_job.resources_viewed'
EXPERIMENT_JOB_LOGS_VIEWED = 'experiment_job.logs_viewed'
EXPERIMENT_JOB_STATUSES_VIEWED = 'experiment_job.statuses_viewed'


class ExperimentJobViewedEvent(Event):
    event_type = EXPERIMENT_JOB_VIEWED
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
    event_type = EXPERIMENT_JOB_RESOURCES_VIEWED
    attributes = (
        Attribute('id'),
        Attribute('sequence'),
        Attribute('experiment.id'),
        Attribute('experiment.user.id'),
        Attribute('actor_id'),
        Attribute('status'),
    )


class ExperimentJobLogsViewedEvent(Event):
    event_type = EXPERIMENT_JOB_LOGS_VIEWED
    attributes = (
        Attribute('id'),
        Attribute('sequence'),
        Attribute('experiment.id'),
        Attribute('experiment.user.id'),
        Attribute('actor_id'),
        Attribute('status'),
    )


class ExperimentJobStatusesViewedEvent(Event):
    event_type = EXPERIMENT_JOB_STATUSES_VIEWED
    attributes = (
        Attribute('id'),
        Attribute('sequence'),
        Attribute('experiment.id'),
        Attribute('experiment.user.id'),
        Attribute('actor_id'),
        Attribute('status'),
    )
