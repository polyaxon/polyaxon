import executor

from events.registry import experiment_job

executor.subscribe(experiment_job.ExperimentJobNewStatusEvent)
