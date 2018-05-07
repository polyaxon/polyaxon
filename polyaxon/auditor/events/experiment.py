import auditor
from libs.event_manager import event_types
from libs.event_manager.event import Event


class ExperimentCreatedEvent(Event):
    type = event_types.EXPERIMENT_CREATED


class ExperimentUpdatedEvent(Event):
    type = event_types.EXPERIMENT_UPDATED


class ExperimentDeletedEvent(Event):
    type = event_types.EXPERIMENT_DELETED


class ExperimentViewedEvent(Event):
    type = event_types.EXPERIMENT_VIEWED


class ExperimentStoppedEvent(Event):
    type = event_types.EXPERIMENT_STOPPED


class ExperimentResumedEvent(Event):
    type = event_types.EXPERIMENT_RESUMED


class ExperimentRestartedEvent(Event):
    type = event_types.EXPERIMENT_RESTARTED


class ExperimentCopiedEvent(Event):
    type = event_types.EXPERIMENT_COPIED


class ExperimentSucceededEvent(Event):
    type = event_types.EXPERIMENT_SUCCEEDED


class ExperimentFailedEvent(Event):
    type = event_types.EXPERIMENT_FAILED


class ExperimentResourcesViewedEvent(Event):
    type = event_types.EXPERIMENT_RESOURCES_VIEWED


class ExperimentLogsViewedEvent(Event):
    type = event_types.EXPERIMENT_LOGS_VIEWED


class ExperimentStatusesViewedEvent(Event):
    type = event_types.EXPERIMENT_STATUSES_VIEWED


class ExperimentJobsViewedEvent(Event):
    type = event_types.EXPERIMENT_JOBS_VIEWED


class ExperimentJobViewedEvent(Event):
    type = event_types.EXPERIMENT_JOB_VIEWED


class ExperimentJobResourcesViewedEvent(Event):
    type = event_types.EXPERIMENT_JOB_RESOURCES_VIEWED


class ExperimentJobLogsViewedEvent(Event):
    type = event_types.EXPERIMENT_JOB_LOGS_VIEWED


class ExperimentJobStatusesViewedEvent(Event):
    type = event_types.EXPERIMENT_JOB_STATUSES_VIEWED


auditor.register(ExperimentCreatedEvent)
auditor.register(ExperimentUpdatedEvent)
auditor.register(ExperimentDeletedEvent)
auditor.register(ExperimentViewedEvent)
auditor.register(ExperimentStoppedEvent)
auditor.register(ExperimentResumedEvent)
auditor.register(ExperimentRestartedEvent)
auditor.register(ExperimentCopiedEvent)
auditor.register(ExperimentSucceededEvent)
auditor.register(ExperimentFailedEvent)
auditor.register(ExperimentResourcesViewedEvent)
auditor.register(ExperimentLogsViewedEvent)
auditor.register(ExperimentStatusesViewedEvent)
auditor.register(ExperimentJobsViewedEvent)

auditor.register(ExperimentJobViewedEvent)
auditor.register(ExperimentJobResourcesViewedEvent)
auditor.register(ExperimentJobLogsViewedEvent)
auditor.register(ExperimentJobStatusesViewedEvent)
