from event_manager import event_actions, event_subjects
from event_manager.event import Attribute, Event

TENSORBOARD_STARTED = '{}.{}'.format(event_subjects.TENSORBOARD, event_actions.STARTED)
TENSORBOARD_STARTED_TRIGGERED = '{}.{}.{}'.format(event_subjects.TENSORBOARD,
                                                  event_actions.STARTED,
                                                  event_subjects.TRIGGER)
TENSORBOARD_STOPPED = '{}.{}'.format(event_subjects.TENSORBOARD, event_actions.STOPPED)
TENSORBOARD_STOPPED_TRIGGERED = '{}.{}.{}'.format(event_subjects.TENSORBOARD,
                                                  event_actions.STOPPED,
                                                  event_subjects.TRIGGER)
TENSORBOARD_VIEWED = '{}.{}'.format(event_subjects.TENSORBOARD, event_actions.VIEWED)
TENSORBOARD_BOOKMARKED = '{}.{}'.format(event_subjects.TENSORBOARD, event_actions.BOOKMARKED)
TENSORBOARD_NEW_STATUS = '{}.{}'.format(event_subjects.TENSORBOARD, event_actions.NEW_STATUS)
TENSORBOARD_FAILED = '{}.{}'.format(event_subjects.TENSORBOARD, event_actions.FAILED)
TENSORBOARD_SUCCEEDED = '{}.{}'.format(event_subjects.TENSORBOARD, event_actions.SUCCEEDED)


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
    actor_id = 'actor_id'
    attributes = (
        Attribute('id'),
        Attribute('user.id'),
        Attribute('project.id'),
        Attribute('project.user.id'),
        Attribute('actor_id'),
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
    actor_id = 'actor_id'
    attributes = (
        Attribute('id'),
        Attribute('user.id'),
        Attribute('project.id'),
        Attribute('project.user.id'),
        Attribute('target'),  # project, experiment_group, experiment
        Attribute('actor_id'),
        Attribute('last_status'),
    )


class TensorboardViewedEvent(Event):
    event_type = TENSORBOARD_VIEWED
    actor_id = 'actor_id'
    attributes = (
        Attribute('id'),
        Attribute('user.id'),
        Attribute('project.id'),
        Attribute('project.user.id'),
        Attribute('actor_id'),
        Attribute('last_status'),
        Attribute('target'),  # project, experiment_group, experiment
    )


class TensorboardBookmarkedEvent(Event):
    event_type = TENSORBOARD_BOOKMARKED
    actor_id = 'actor_id'
    attributes = (
        Attribute('id'),
        Attribute('user.id'),
        Attribute('project.id'),
        Attribute('project.user.id'),
        Attribute('actor_id'),
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
