from event_manager import event_actions, event_subjects
from event_manager.event import Attribute, Event

EXPERIMENT_GROUP_CREATED = '{}.{}'.format(event_subjects.EXPERIMENT_GROUP,
                                          event_actions.CREATED)
EXPERIMENT_GROUP_UPDATED = '{}.{}'.format(event_subjects.EXPERIMENT_GROUP,
                                          event_actions.UPDATED)
EXPERIMENT_GROUP_DELETED = '{}.{}'.format(event_subjects.EXPERIMENT_GROUP,
                                          event_actions.DELETED)
EXPERIMENT_GROUP_VIEWED = '{}.{}'.format(event_subjects.EXPERIMENT_GROUP,
                                         event_actions.VIEWED)
EXPERIMENT_GROUP_STOPPED = '{}.{}'.format(event_subjects.EXPERIMENT_GROUP,
                                          event_actions.STOPPED)
EXPERIMENT_GROUP_RESUMED = '{}.{}'.format(event_subjects.EXPERIMENT_GROUP,
                                          event_actions.RESUMED)
EXPERIMENT_GROUP_FINISHED = '{}.{}'.format(event_subjects.EXPERIMENT_GROUP,
                                           event_actions.FINISHED)
EXPERIMENT_GROUP_NEW_STATUS = '{}.{}'.format(event_subjects.EXPERIMENT_GROUP,
                                             event_actions.NEW_STATUS)
EXPERIMENT_GROUP_EXPERIMENTS_VIEWED = '{}.{}'.format(event_subjects.EXPERIMENT_GROUP,
                                                     event_actions.EXPERIMENTS_VIEWED)
EXPERIMENT_GROUP_ITERATION = '{}.new_iteration'.format(event_subjects.EXPERIMENT_GROUP)
EXPERIMENT_GROUP_RANDOM = '{}.random'.format(event_subjects.EXPERIMENT_GROUP)
EXPERIMENT_GROUP_GRID = '{}.grid'.format(event_subjects.EXPERIMENT_GROUP)
EXPERIMENT_GROUP_HYPERBAND = '{}.hyperband'.format(event_subjects.EXPERIMENT_GROUP)
EXPERIMENT_GROUP_BO = '{}.bo'.format(event_subjects.EXPERIMENT_GROUP)


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


class ExperimentGroupNewStatusEvent(Event):
    event_type = EXPERIMENT_GROUP_NEW_STATUS
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
    event_type = EXPERIMENT_GROUP_EXPERIMENTS_VIEWED
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
