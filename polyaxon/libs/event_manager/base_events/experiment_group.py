from libs.event_manager.event import Event

EXPERIMENT_GROUP_CREATED = 'experiment_group.created'
EXPERIMENT_GROUP_UPDATED = 'experiment_group.updated'
EXPERIMENT_GROUP_DELETED = 'experiment_group.deleted'
EXPERIMENT_GROUP_VIEWED = 'experiment_group.viewed'
EXPERIMENT_GROUP_STOPPED = 'experiment_group.stopped'
EXPERIMENT_GROUP_RESUMED = 'experiment_group.resumed'
EXPERIMENT_GROUP_RANDOM = 'experiment_group.random'
EXPERIMENT_GROUP_GRID = 'experiment_group.grid'
EXPERIMENT_GROUP_HYPERBAND = 'experiment_group.hyperband'
EXPERIMENT_GROUP_BO = 'experiment_group.bo'
EXPERIMENT_GROUP_ITERATION = 'experiment_group.iteration'
EXPERIMENT_GROUP_FINISHED = 'experiment_group.finished'
EXPERIMENT_GROUP_EXPERIMENTS = 'experiment_group.experiments'


class ExperimentGroupCreatedEvent(Event):
    type = EXPERIMENT_GROUP_CREATED


class ExperimentGroupUpdatedEvent(Event):
    type = EXPERIMENT_GROUP_UPDATED


class ExperimentGroupDeletedEvent(Event):
    type = EXPERIMENT_GROUP_DELETED


class ExperimentGroupViewedEvent(Event):
    type = EXPERIMENT_GROUP_VIEWED


class ExperimentGroupStoppedEvent(Event):
    type = EXPERIMENT_GROUP_STOPPED


class ExperimentGroupResumedEvent(Event):
    type = EXPERIMENT_GROUP_RESUMED


class ExperimentGroupFinishedEvent(Event):
    type = EXPERIMENT_GROUP_FINISHED


class ExperimentGroupIterationEvent(Event):
    type = EXPERIMENT_GROUP_ITERATION


class ExperimentGroupExperimentsViewedEvent(Event):
    type = EXPERIMENT_GROUP_EXPERIMENTS


class ExperimentGroupRandomEvent(Event):
    type = EXPERIMENT_GROUP_RANDOM


class ExperimentGroupGridEvent(Event):
    type = EXPERIMENT_GROUP_GRID


class ExperimentGroupHyperbandEvent(Event):
    type = EXPERIMENT_GROUP_HYPERBAND


class ExperimentGroupBOEvent(Event):
    type = EXPERIMENT_GROUP_BO
