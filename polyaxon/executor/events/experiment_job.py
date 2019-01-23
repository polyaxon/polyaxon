import executor

from event_manager.events import experiment_job

executor.subscribe(experiment_job.ExperimentJobNewStatusEvent)
