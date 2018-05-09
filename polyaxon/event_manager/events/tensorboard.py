from event_manager import event_actions, event_subjects
from event_manager.event import Attribute, Event

TENSORBOARD_STARTED = '{}.{}'.format(event_subjects.TENSORBOARD, event_actions.STARTED)
TENSORBOARD_STOPPED = '{}.{}'.format(event_subjects.TENSORBOARD, event_actions.STOPPED)
TENSORBOARD_VIEWED = '{}.{}'.format(event_subjects.TENSORBOARD, event_actions.VIEWED)
TENSORBOARD_NEW_STATUS = '{}.{}'.format(event_subjects.TENSORBOARD, event_actions.NEW_STATUS)


class TensorboardStartedEvent(Event):
    event_type = TENSORBOARD_STARTED
    actor_id = 'actor_id'
    attributes = (
        Attribute('id'),
        Attribute('project.id'),
        Attribute('project.user.id'),
        Attribute('actor_id')
    )


class TensorboardSoppedEvent(Event):
    event_type = TENSORBOARD_STOPPED
    actor_id = 'actor_id'
    attributes = (
        Attribute('id'),
        Attribute('project.id'),
        Attribute('project.user.id'),
        Attribute('actor_id'),
        Attribute('status'),
    )


class TensorboardViewedEvent(Event):
    event_type = TENSORBOARD_VIEWED
    actor_id = 'actor_id'
    attributes = (
        Attribute('id'),
        Attribute('project.id'),
        Attribute('project.user.id'),
        Attribute('actor_id'),
        Attribute('status'),
    )


class TensorboardNewStatusEvent(Event):
    event_type = TENSORBOARD_NEW_STATUS
    attributes = (
        Attribute('id'),
        Attribute('project.id'),
        Attribute('status'),
    )
