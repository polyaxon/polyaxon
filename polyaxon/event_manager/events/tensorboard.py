from event_manager.event import Attribute, Event

TENSORBOARD_STARTED = 'tensorboard.started'
TENSORBOARD_STOPPED = 'tensorboard.stopped'
TENSORBOARD_VIEWED = 'tensorboard.viewed'
TENSORBOARD_NEW_STATUS = 'tensorboard.new_status'


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
