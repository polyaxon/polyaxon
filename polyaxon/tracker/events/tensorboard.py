import tracker

from event_manager.events import tensorboard

tracker.subscribe(tensorboard.TensorboardStartedEvent)
tracker.subscribe(tensorboard.TensorboardSoppedEvent)
tracker.subscribe(tensorboard.TensorboardViewedEvent)
tracker.subscribe(tensorboard.TensorboardNewStatusEvent)
