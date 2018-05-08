from event_manager.event import Event

TENSORBOARD_STARTED = 'tensorboard.started'
TENSORBOARD_STOPPED = 'tensorboard.stopped'
TENSORBOARD_NEW_STATUS = 'tensorboard.new_status'


class TensorboardStartedEvent(Event):
    type = TENSORBOARD_STARTED


class TensorboardSoppedEvent(Event):
    type = TENSORBOARD_STOPPED


class TensorboardNewStatusEvent(Event):
    type = TENSORBOARD_NEW_STATUS
