from event_manager.event import Event, Attribute

TENSORBOARD_STARTED = 'tensorboard.started'
TENSORBOARD_STOPPED = 'tensorboard.stopped'
TENSORBOARD_NEW_STATUS = 'tensorboard.new_status'


class TensorboardStartedEvent(Event):
    type = TENSORBOARD_STARTED
    attributes = (
        Attribute('tensorboard_uuid', is_uuid=True),
        Attribute('project_uuid', is_uuid=True),
        Attribute('project_owner_uuid', is_uuid=True),
        Attribute('actor_uuid')
    )


class TensorboardSoppedEvent(Event):
    type = TENSORBOARD_STOPPED
    attributes = (
        Attribute('tensorboard_uuid', is_uuid=True),
        Attribute('project_uuid', is_uuid=True),
        Attribute('project_owner_uuid', is_uuid=True),
        Attribute('actor_uuid')
    )


class TensorboardNewStatusEvent(Event):
    type = TENSORBOARD_NEW_STATUS
    attributes = (
        Attribute('tensorboard_uuid', is_uuid=True),
        Attribute('project_uuid', is_uuid=True),
        Attribute('statue')
    )
