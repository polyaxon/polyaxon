import auditor
from event_manager.events import tensorboard

auditor.register(tensorboard.TensorboardStartedEvent)
auditor.register(tensorboard.TensorboardSoppedEvent)
auditor.register(tensorboard.TensorboardViewedEvent)
auditor.register(tensorboard.TensorboardNewStatusEvent)
