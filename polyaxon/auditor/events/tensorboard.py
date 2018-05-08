import auditor
from libs.event_manager.base_events import tensorboard

auditor.register(tensorboard.TensorboardStartedEvent)
auditor.register(tensorboard.TensorboardSoppedEvent)
auditor.register(tensorboard.TensorboardNewStatusEvent)
