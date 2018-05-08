import auditor
from libs.event_manager import event_types
from libs.event_manager.event import Event


class TensorboardStartedEvent(Event):
    type = event_types.TENSORBOARD_STARTED


class TensorboardSoppedEvent(Event):
    type = event_types.TENSORBOARD_STOPPED


class TensorboardNewStatusEvent(Event):
    type = event_types.TENSORBOARD_NEW_STATUS


auditor.register(TensorboardStartedEvent)
auditor.register(TensorboardSoppedEvent)
auditor.register(TensorboardNewStatusEvent)
