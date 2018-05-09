from event_manager import event_actions, event_subjects
from event_manager.event import Attribute, Event

EXPERIMENT_CREATED = '{}.{}'.format(event_subjects.EXPERIMENT,
                                    event_actions.CREATED)
EXPERIMENT_UPDATED = '{}.{}'.format(event_subjects.EXPERIMENT,
                                    event_actions.UPDATED)
EXPERIMENT_DELETED = '{}.{}'.format(event_subjects.EXPERIMENT,
                                    event_actions.DELETED)
EXPERIMENT_VIEWED = '{}.{}'.format(event_subjects.EXPERIMENT,
                                   event_actions.VIEWED)
EXPERIMENT_STOPPED = '{}.{}'.format(event_subjects.EXPERIMENT,
                                    event_actions.STOPPED)
EXPERIMENT_RESUMED = '{}.{}'.format(event_subjects.EXPERIMENT,
                                    event_actions.RESUMED)
EXPERIMENT_RESTARTED = '{}.{}'.format(event_subjects.EXPERIMENT,
                                      event_actions.RESTARTED)
EXPERIMENT_COPIED = '{}.{}'.format(event_subjects.EXPERIMENT,
                                   event_actions.COPIED)
EXPERIMENT_NEW_STATUS = '{}.{}'.format(event_subjects.EXPERIMENT,
                                       event_actions.NEW_STATUS)
EXPERIMENT_SUCCEEDED = '{}.{}'.format(event_subjects.EXPERIMENT,
                                      event_actions.SUCCEEDED)
EXPERIMENT_FAILED = '{}.{}'.format(event_subjects.EXPERIMENT,
                                   event_actions.FAILED)
EXPERIMENT_RESOURCES_VIEWED = '{}.{}'.format(event_subjects.EXPERIMENT,
                                             event_actions.RESOURCES_VIEWED)
EXPERIMENT_LOGS_VIEWED = '{}.{}'.format(event_subjects.EXPERIMENT,
                                        event_actions.LOGS_VIEWED)
EXPERIMENT_STATUSES_VIEWED = '{}.{}'.format(event_subjects.EXPERIMENT,
                                            event_actions.STATUSES_VIEWED)
EXPERIMENT_JOBS_VIEWED = '{}.{}'.format(event_subjects.EXPERIMENT,
                                        event_actions.JOBS_VIEWED)


class ExperimentCreatedEvent(Event):
    event_type = EXPERIMENT_CREATED
    actor_id = 'user.id'
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
    event_type = EXPERIMENT_UPDATED
    actor_id = 'actor_id'
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
    event_type = EXPERIMENT_DELETED
    actor_id = 'actor_id'
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
    event_type = EXPERIMENT_VIEWED
    actor_id = 'actor_id'
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
    event_type = EXPERIMENT_STOPPED
    actor_id = 'actor_id'
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
    event_type = EXPERIMENT_RESUMED
    actor_id = 'actor_id'
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
    event_type = EXPERIMENT_RESTARTED
    actor_id = 'actor_id'
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
    event_type = EXPERIMENT_COPIED
    actor_id = 'actor_id'
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
    event_type = EXPERIMENT_NEW_STATUS
    attributes = (
        Attribute('id'),
        Attribute('sequence'),
        Attribute('project.id'),
        Attribute('experiment_group.id'),
        Attribute('status'),
    )


class ExperimentSucceededEvent(Event):
    event_type = EXPERIMENT_SUCCEEDED
    attributes = (
        Attribute('id'),
        Attribute('sequence'),
        Attribute('project.id'),
        Attribute('experiment_group.id'),
    )


class ExperimentFailedEvent(Event):
    event_type = EXPERIMENT_FAILED
    attributes = (
        Attribute('id'),
        Attribute('sequence'),
        Attribute('project.id'),
        Attribute('experiment_group.id'),
    )


class ExperimentResourcesViewedEvent(Event):
    event_type = EXPERIMENT_RESOURCES_VIEWED
    actor_id = 'actor_id'
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
    event_type = EXPERIMENT_LOGS_VIEWED
    actor_id = 'actor_id'
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
    event_type = EXPERIMENT_STATUSES_VIEWED
    actor_id = 'actor_id'
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
    event_type = EXPERIMENT_JOBS_VIEWED
    actor_id = 'actor_id'
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
