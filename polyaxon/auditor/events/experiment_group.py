import auditor
from libs.event_manager import event_types
from libs.event_manager.event import Event


class ExperimentGroupCreatedEvent(Event):
    type = event_types.EXPERIMENT_GROUP_CREATED


class ExperimentGroupUpdatedEvent(Event):
    type = event_types.EXPERIMENT_GROUP_UPDATED


class ExperimentGroupDeletedEvent(Event):
    type = event_types.EXPERIMENT_GROUP_DELETED


class ExperimentGroupViewedEvent(Event):
    type = event_types.EXPERIMENT_GROUP_VIEWED


class ExperimentGroupStoppedEvent(Event):
    type = event_types.EXPERIMENT_GROUP_STOPPED


class ExperimentGroupResumedEvent(Event):
    type = event_types.EXPERIMENT_GROUP_RESUMED


class ExperimentGroupFinishedEvent(Event):
    type = event_types.EXPERIMENT_GROUP_FINISHED


class ExperimentGroupIterationEvent(Event):
    type = event_types.EXPERIMENT_GROUP_ITERATION


class ExperimentGroupExperimentsViewedEvent(Event):
    type = event_types.EXPERIMENT_GROUP_EXPERIMENTS


class ExperimentGroupRandomEvent(Event):
    type = event_types.EXPERIMENT_GROUP_RANDOM


class ExperimentGroupGridEvent(Event):
    type = event_types.EXPERIMENT_GROUP_GRID


class ExperimentGroupHyperbandEvent(Event):
    type = event_types.EXPERIMENT_GROUP_HYPERBAND


class ExperimentGroupBOEvent(Event):
    type = event_types.EXPERIMENT_GROUP_BO


auditor.register(ExperimentGroupCreatedEvent)
auditor.register(ExperimentGroupUpdatedEvent)
auditor.register(ExperimentGroupDeletedEvent)
auditor.register(ExperimentGroupViewedEvent)
auditor.register(ExperimentGroupStoppedEvent)
auditor.register(ExperimentGroupResumedEvent)
auditor.register(ExperimentGroupFinishedEvent)
auditor.register(ExperimentGroupExperimentsViewedEvent)
auditor.register(ExperimentGroupIterationEvent)
auditor.register(ExperimentGroupRandomEvent)
auditor.register(ExperimentGroupGridEvent)
auditor.register(ExperimentGroupHyperbandEvent)
auditor.register(ExperimentGroupBOEvent)
