import notifier

from event_manager.events import experiment

# notifier.subscribe_event(experiment.ExperimentNewStatusEvent)
# notifier.subscribe_event(experiment.ExperimentNewMetricEvent)
# notifier.subscribe_event(experiment.ExperimentDoneEvent)
notifier.subscribe_event(experiment.ExperimentStoppedEvent)
notifier.subscribe_event(experiment.ExperimentSucceededEvent)
notifier.subscribe_event(experiment.ExperimentFailedEvent)
