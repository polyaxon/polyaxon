from events import event_actions, event_subjects
from events.event import Attribute, Event

TENSORBOARD_STARTED = '{}.{}'.format(event_subjects.TENSORBOARD, event_actions.STARTED)
TENSORBOARD_STARTED_TRIGGERED = '{}.{}.{}'.format(event_subjects.TENSORBOARD,
                                                  event_actions.STARTED,
                                                  event_subjects.TRIGGER)
TENSORBOARD_STOPPED = '{}.{}'.format(event_subjects.TENSORBOARD, event_actions.STOPPED)
TENSORBOARD_STOPPED_TRIGGERED = '{}.{}.{}'.format(event_subjects.TENSORBOARD,
                                                  event_actions.STOPPED,
                                                  event_subjects.TRIGGER)
TENSORBOARD_CLEANED_TRIGGERED = '{}.{}.{}'.format(event_subjects.TENSORBOARD,
                                                  event_actions.CLEANED,
                                                  event_subjects.TRIGGER)
TENSORBOARD_VIEWED = '{}.{}'.format(event_subjects.TENSORBOARD, event_actions.VIEWED)
TENSORBOARD_UPDATED = '{}.{}'.format(event_subjects.TENSORBOARD, event_actions.UPDATED)
TENSORBOARD_DELETED = '{}.{}'.format(event_subjects.TENSORBOARD, event_actions.DELETED)
TENSORBOARD_DELETED_TRIGGERED = '{}.{}.{}'.format(event_subjects.TENSORBOARD,
                                                  event_actions.DELETED,
                                                  event_subjects.TRIGGER)
TENSORBOARD_ARCHIVED = '{}.{}'.format(event_subjects.TENSORBOARD, event_actions.ARCHIVED)
TENSORBOARD_RESTORED = '{}.{}'.format(event_subjects.TENSORBOARD, event_actions.RESTORED)
TENSORBOARD_BOOKMARKED = '{}.{}'.format(event_subjects.TENSORBOARD, event_actions.BOOKMARKED)
TENSORBOARD_UNBOOKMARKED = '{}.{}'.format(event_subjects.TENSORBOARD, event_actions.UNBOOKMARKED)
TENSORBOARD_NEW_STATUS = '{}.{}'.format(event_subjects.TENSORBOARD, event_actions.NEW_STATUS)
TENSORBOARD_FAILED = '{}.{}'.format(event_subjects.TENSORBOARD, event_actions.FAILED)
TENSORBOARD_SUCCEEDED = '{}.{}'.format(event_subjects.TENSORBOARD, event_actions.SUCCEEDED)
TENSORBOARD_STATUSES_VIEWED = '{}.{}'.format(event_subjects.TENSORBOARD,
                                             event_actions.STATUSES_VIEWED)

EVENTS = {
    TENSORBOARD_STARTED,
    TENSORBOARD_STARTED_TRIGGERED,
    TENSORBOARD_STOPPED,
    TENSORBOARD_STOPPED_TRIGGERED,
    TENSORBOARD_CLEANED_TRIGGERED,
    TENSORBOARD_VIEWED,
    TENSORBOARD_UPDATED,
    TENSORBOARD_DELETED,
    TENSORBOARD_DELETED_TRIGGERED,
    TENSORBOARD_ARCHIVED,
    TENSORBOARD_RESTORED,
    TENSORBOARD_BOOKMARKED,
    TENSORBOARD_UNBOOKMARKED,
    TENSORBOARD_NEW_STATUS,
    TENSORBOARD_FAILED,
    TENSORBOARD_SUCCEEDED,
    TENSORBOARD_STATUSES_VIEWED,
}


class TensorboardStartedEvent(Event):
    event_type = TENSORBOARD_STARTED
    attributes = (
        Attribute('id'),
        Attribute('user.id'),
        Attribute('project.id'),
        Attribute('project.user.id'),
        Attribute('target'),  # project, experiment_group, experiment
    )


class TensorboardStartedTriggeredEvent(Event):
    event_type = TENSORBOARD_STARTED_TRIGGERED
    actor = True
    attributes = (
        Attribute('id'),
        Attribute('user.id'),
        Attribute('project.id'),
        Attribute('project.user.id'),
        Attribute('target'),  # project, experiment_group, experiment
    )


class TensorboardSoppedEvent(Event):
    event_type = TENSORBOARD_STOPPED
    attributes = (
        Attribute('id'),
        Attribute('user.id'),
        Attribute('project.id'),
        Attribute('project.user.id'),
        Attribute('target'),  # project, experiment_group, experiment
        Attribute('last_status'),
        Attribute('previous_status', is_required=False),
    )


class TensorboardSoppedTriggeredEvent(Event):
    event_type = TENSORBOARD_STOPPED_TRIGGERED
    actor = True
    attributes = (
        Attribute('id'),
        Attribute('user.id'),
        Attribute('project.id'),
        Attribute('project.user.id'),
        Attribute('target'),  # project, experiment_group, experiment
        Attribute('last_status'),
    )


class TensorboardCleanedTriggeredEvent(Event):
    event_type = TENSORBOARD_CLEANED_TRIGGERED
    attributes = (
        Attribute('id'),
    )


class TensorboardViewedEvent(Event):
    event_type = TENSORBOARD_VIEWED
    actor = True
    attributes = (
        Attribute('id'),
        Attribute('user.id'),
        Attribute('project.id'),
        Attribute('project.user.id'),
        Attribute('last_status'),
    )


class TensorboardUpdatedEvent(Event):
    event_type = TENSORBOARD_UPDATED
    actor = True
    attributes = (
        Attribute('id'),
        Attribute('user.id'),
        Attribute('project.id'),
        Attribute('project.user.id'),
        Attribute('last_status'),
    )


class TensorboardDeletedTriggeredEvent(Event):
    event_type = TENSORBOARD_DELETED_TRIGGERED
    actor = True
    attributes = (
        Attribute('id'),
        Attribute('user.id'),
        Attribute('project.id'),
        Attribute('project.user.id'),
        Attribute('last_status'),
    )


class TensorboardDeletedEvent(Event):
    event_type = TENSORBOARD_DELETED
    attributes = (
        Attribute('id'),
    )


class TensorboardBookmarkedEvent(Event):
    event_type = TENSORBOARD_BOOKMARKED
    actor = True
    attributes = (
        Attribute('id'),
        Attribute('user.id'),
        Attribute('project.id'),
        Attribute('project.user.id'),
        Attribute('last_status'),
        Attribute('target'),  # project, experiment_group, experiment
    )


class TensorboardUnBookmarkedEvent(Event):
    event_type = TENSORBOARD_UNBOOKMARKED
    actor = True
    attributes = (
        Attribute('id'),
        Attribute('user.id'),
        Attribute('project.id'),
        Attribute('project.user.id'),
        Attribute('last_status'),
        Attribute('target'),  # project, experiment_group, experiment
    )


class TensorboardNewStatusEvent(Event):
    event_type = TENSORBOARD_NEW_STATUS
    attributes = (
        Attribute('id'),
        Attribute('user.id'),
        Attribute('project.id'),
        Attribute('last_status'),
        Attribute('target'),  # project, experiment_group, experiment
    )


class TensorboardSucceededEvent(Event):
    event_type = TENSORBOARD_SUCCEEDED
    attributes = (
        Attribute('id'),
        Attribute('user.id'),
        Attribute('project.id'),
        Attribute('last_status'),
        Attribute('previous_status', is_required=False),
        Attribute('target'),  # project, experiment_group, experiment
    )


class TensorboardFailedEvent(Event):
    event_type = TENSORBOARD_FAILED
    attributes = (
        Attribute('id'),
        Attribute('user.id'),
        Attribute('project.id'),
        Attribute('last_status'),
        Attribute('previous_status', is_required=False),
        Attribute('target'),  # project, experiment_group, experiment
    )


class TensorboardStatusesViewedEvent(Event):
    event_type = TENSORBOARD_STATUSES_VIEWED
    actor = True
    attributes = (
        Attribute('id'),
        Attribute('project.id'),
        Attribute('project.user.id'),
        Attribute('user.id'),
        Attribute('last_status'),
        Attribute('target'),  # project, experiment_group, experiment
    )


class TensorboardArchivedEvent(Event):
    event_type = TENSORBOARD_ARCHIVED
    actor = True
    attributes = (
        Attribute('id'),
        Attribute('user.id'),
        Attribute('project.id'),
        Attribute('project.user.id'),
        Attribute('last_status'),
    )


class TensorboardRestoredEvent(Event):
    event_type = TENSORBOARD_RESTORED
    actor = True
    attributes = (
        Attribute('id'),
        Attribute('user.id'),
        Attribute('project.id'),
        Attribute('project.user.id'),
        Attribute('last_status'),
    )
