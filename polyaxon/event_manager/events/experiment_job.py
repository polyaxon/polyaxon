from event_manager import event_subjects, event_actions
from event_manager.event import Attribute, Event

EXPERIMENT_JOB_VIEWED = '{}.{}'.format(event_subjects.EXPERIMENT_JOB,
                                       event_actions.VIEWED)
EXPERIMENT_JOB_RESOURCES_VIEWED = '{}.{}'.format(event_subjects.EXPERIMENT_JOB,
                                                 event_actions.RESOURCES_VIEWED)
EXPERIMENT_JOB_LOGS_VIEWED = '{}.{}'.format(event_subjects.EXPERIMENT_JOB,
                                            event_actions.LOGS_VIEWED)
EXPERIMENT_JOB_STATUSES_VIEWED = '{}.{}'.format(event_subjects.EXPERIMENT_JOB,
                                                event_actions.STATUSES_VIEWED)


class ExperimentJobViewedEvent(Event):
    event_type = EXPERIMENT_JOB_VIEWED
    actor_id = 'actor_id'
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
    actor_id = 'actor_id'
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
    actor_id = 'actor_id'
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
    actor_id = 'actor_id'
    attributes = (
        Attribute('id'),
        Attribute('sequence'),
        Attribute('experiment.id'),
        Attribute('experiment.user.id'),
        Attribute('actor_id'),
        Attribute('status'),
    )
