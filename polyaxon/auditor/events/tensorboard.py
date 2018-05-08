import auditor

from event_manager.events import tensorboard

auditor.subscribe(tensorboard.TensorboardStartedEvent)
auditor.subscribe(tensorboard.TensorboardSoppedEvent)
auditor.subscribe(tensorboard.TensorboardViewedEvent)
auditor.subscribe(tensorboard.TensorboardNewStatusEvent)
