from event_manager.event import Attribute, Event

EXPERIMENT_GROUP_CREATED = 'experiment_group.created'
EXPERIMENT_GROUP_UPDATED = 'experiment_group.updated'
EXPERIMENT_GROUP_DELETED = 'experiment_group.deleted'
EXPERIMENT_GROUP_VIEWED = 'experiment_group.viewed'
EXPERIMENT_GROUP_STOPPED = 'experiment_group.stopped'
EXPERIMENT_GROUP_RESUMED = 'experiment_group.resumed'
EXPERIMENT_GROUP_FINISHED = 'experiment_group.finished'
EXPERIMENT_GROUP_EXPERIMENTS = 'experiment_group.experiments'
EXPERIMENT_GROUP_ITERATION = 'experiment_group.iteration'
EXPERIMENT_GROUP_RANDOM = 'experiment_group.random'
EXPERIMENT_GROUP_GRID = 'experiment_group.grid'
EXPERIMENT_GROUP_HYPERBAND = 'experiment_group.hyperband'
EXPERIMENT_GROUP_BO = 'experiment_group.bo'


class ExperimentGroupCreatedEvent(Event):
    event_type = EXPERIMENT_GROUP_CREATED
    actor_id = 'user.id'
    attributes = (
        Attribute('id'),
        Attribute('sequence'),
        Attribute('project.id'),
        Attribute('project.user.id'),
        Attribute('user.id'),
        Attribute('created_at', is_datetime=True),
        Attribute('concurrency'),
        Attribute('search_algorithm'),
        Attribute('has_early_stopping', attr_type=bool),
        Attribute('has_description', attr_type=bool),
        Attribute('is_resume', attr_type=bool),
        Attribute('is_restart', attr_type=bool),
    )


class ExperimentGroupUpdatedEvent(Event):
    event_type = EXPERIMENT_GROUP_UPDATED
    actor_id = 'actor_id'
    attributes = (
        Attribute('id'),
        Attribute('sequence'),
        Attribute('project.id'),
        Attribute('project.user.id'),
        Attribute('user.id'),
        Attribute('actor_id'),
        Attribute('updated_at', is_datetime=True),
        Attribute('concurrency'),
        Attribute('search_algorithm'),
        Attribute('has_early_stopping', attr_type=bool),
        Attribute('has_description', attr_type=bool),
        Attribute('is_resume', attr_type=bool),
        Attribute('is_restart', attr_type=bool),
        Attribute('status'),
    )


class ExperimentGroupDeletedEvent(Event):
    event_type = EXPERIMENT_GROUP_DELETED
    actor_id = 'actor_id'
    attributes = (
        Attribute('id'),
        Attribute('sequence'),
        Attribute('project.id'),
        Attribute('project.user.id'),
        Attribute('user.id'),
        Attribute('actor_id'),
        Attribute('updated_at', is_datetime=True),
        Attribute('concurrency'),
        Attribute('search_algorithm'),
        Attribute('has_early_stopping', attr_type=bool),
        Attribute('has_description', attr_type=bool),
        Attribute('is_resume', attr_type=bool),
        Attribute('is_restart', attr_type=bool),
        Attribute('status'),
    )


class ExperimentGroupViewedEvent(Event):
    event_type = EXPERIMENT_GROUP_VIEWED
    actor_id = 'actor_id'
    attributes = (
        Attribute('id'),
        Attribute('sequence'),
        Attribute('project.id'),
        Attribute('project.user.id'),
        Attribute('user.id'),
        Attribute('actor_id'),
        Attribute('updated_at', is_datetime=True),
        Attribute('concurrency'),
        Attribute('search_algorithm'),
        Attribute('has_early_stopping', attr_type=bool),
        Attribute('has_description', attr_type=bool),
        Attribute('is_resume', attr_type=bool),
        Attribute('is_restart', attr_type=bool),
        Attribute('status'),
    )


class ExperimentGroupStoppedEvent(Event):
    event_type = EXPERIMENT_GROUP_STOPPED
    actor_id = 'actor_id'
    attributes = (
        Attribute('id'),
        Attribute('sequence'),
        Attribute('project.id'),
        Attribute('project.user.id'),
        Attribute('user.id'),
        Attribute('actor_id'),
        Attribute('updated_at', is_datetime=True),
        Attribute('concurrency'),
        Attribute('search_algorithm'),
        Attribute('has_early_stopping', attr_type=bool),
        Attribute('has_description', attr_type=bool),
        Attribute('is_resume', attr_type=bool),
        Attribute('is_restart', attr_type=bool),
        Attribute('status'),
    )


class ExperimentGroupResumedEvent(Event):
    event_type = EXPERIMENT_GROUP_RESUMED
    actor_id = 'actor_id'
    attributes = (
        Attribute('id'),
        Attribute('sequence'),
        Attribute('project.id'),
        Attribute('project.user.id'),
        Attribute('user.id'),
        Attribute('actor_id'),
        Attribute('updated_at', is_datetime=True),
        Attribute('concurrency'),
        Attribute('search_algorithm'),
        Attribute('has_early_stopping', attr_type=bool),
        Attribute('has_description', attr_type=bool),
        Attribute('is_resume', attr_type=bool),
        Attribute('is_restart', attr_type=bool),
        Attribute('status'),
    )


class ExperimentGroupFinishedEvent(Event):
    event_type = EXPERIMENT_GROUP_FINISHED
    attributes = (
        Attribute('id'),
        Attribute('sequence'),
        Attribute('project.id'),
        Attribute('project.user.id'),
        Attribute('user.id'),
        Attribute('updated_at', is_datetime=True),
        Attribute('concurrency'),
        Attribute('search_algorithm'),
        Attribute('has_early_stopping', attr_type=bool),
        Attribute('has_description', attr_type=bool),
        Attribute('is_resume', attr_type=bool),
        Attribute('is_restart', attr_type=bool),
        Attribute('status'),
    )


class ExperimentGroupIterationEvent(Event):
    event_type = EXPERIMENT_GROUP_ITERATION
    attributes = (
        Attribute('id'),
        Attribute('sequence'),
        Attribute('project.id'),
        Attribute('project.user.id'),
        Attribute('user.id'),
        Attribute('updated_at', is_datetime=True),
        Attribute('concurrency'),
        Attribute('search_algorithm'),
        Attribute('has_early_stopping', attr_type=bool),
        Attribute('has_description', attr_type=bool),
        Attribute('is_resume', attr_type=bool),
        Attribute('is_restart', attr_type=bool),
        Attribute('status'),
    )


class ExperimentGroupExperimentsViewedEvent(Event):
    event_type = EXPERIMENT_GROUP_EXPERIMENTS
    actor_id = 'actor_id'
    attributes = (
        Attribute('id'),
        Attribute('sequence'),
        Attribute('project.id'),
        Attribute('project.user.id'),
        Attribute('user.id'),
        Attribute('actor_id'),
        Attribute('updated_at', is_datetime=True),
        Attribute('concurrency'),
        Attribute('search_algorithm'),
        Attribute('has_early_stopping', attr_type=bool),
        Attribute('has_description', attr_type=bool),
        Attribute('is_resume', attr_type=bool),
        Attribute('is_restart', attr_type=bool),
        Attribute('status'),
    )


class ExperimentGroupRandomEvent(Event):
    event_type = EXPERIMENT_GROUP_RANDOM


class ExperimentGroupGridEvent(Event):
    event_type = EXPERIMENT_GROUP_GRID


class ExperimentGroupHyperbandEvent(Event):
    event_type = EXPERIMENT_GROUP_HYPERBAND


class ExperimentGroupBOEvent(Event):
    event_type = EXPERIMENT_GROUP_BO
