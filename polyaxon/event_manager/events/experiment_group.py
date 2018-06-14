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
EXPERIMENT_GROUP_DONE = '{}.{}'.format(event_subjects.EXPERIMENT_GROUP,
                                       event_actions.DONE)
EXPERIMENT_GROUP_NEW_STATUS = '{}.{}'.format(event_subjects.EXPERIMENT_GROUP,
                                             event_actions.NEW_STATUS)
EXPERIMENT_GROUP_EXPERIMENTS_VIEWED = '{}.{}'.format(event_subjects.EXPERIMENT_GROUP,
                                                     event_actions.EXPERIMENTS_VIEWED)
EXPERIMENT_GROUP_ITERATION = '{}.new_iteration'.format(event_subjects.EXPERIMENT_GROUP)
EXPERIMENT_GROUP_RANDOM = '{}.random'.format(event_subjects.EXPERIMENT_GROUP)
EXPERIMENT_GROUP_GRID = '{}.grid'.format(event_subjects.EXPERIMENT_GROUP)
EXPERIMENT_GROUP_HYPERBAND = '{}.hyperband'.format(event_subjects.EXPERIMENT_GROUP)
EXPERIMENT_GROUP_BO = '{}.bo'.format(event_subjects.EXPERIMENT_GROUP)

EXPERIMENT_GROUP_DELETED_TRIGGERED = '{}.{}.{}'.format(event_subjects.EXPERIMENT_GROUP,
                                                       event_actions.DELETED,
                                                       event_subjects.TRIGGER)
EXPERIMENT_GROUP_STOPPED_TRIGGERED = '{}.{}.{}'.format(event_subjects.EXPERIMENT_GROUP,
                                                       event_actions.STOPPED,
                                                       event_subjects.TRIGGER)
EXPERIMENT_GROUP_RESUMED_TRIGGERED = '{}.{}.{}'.format(event_subjects.EXPERIMENT_GROUP,
                                                       event_actions.RESUMED,
                                                       event_subjects.TRIGGER)


class ExperimentGroupCreatedEvent(Event):
    event_type = EXPERIMENT_GROUP_CREATED
    actor_id = 'user.id'
    attributes = (
        Attribute('id'),
        Attribute('sequence'),
        Attribute('project.id'),
        Attribute('project.user.id'),
        Attribute('user.id'),
        Attribute('updated_at', is_datetime=True),
        Attribute('concurrency', is_required=False),
        Attribute('search_algorithm', is_required=False),
        Attribute('has_early_stopping', attr_type=bool, is_required=False),
        Attribute('has_description', attr_type=bool),
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
        Attribute('concurrency', is_required=False),
        Attribute('search_algorithm', is_required=False),
        Attribute('has_early_stopping', attr_type=bool, is_required=False),
        Attribute('has_description', attr_type=bool),
        Attribute('last_status'),
    )


class ExperimentGroupDeletedEvent(Event):
    event_type = EXPERIMENT_GROUP_DELETED
    attributes = (
        Attribute('id'),
        Attribute('sequence'),
        Attribute('updated_at', is_datetime=True),
        Attribute('concurrency', is_required=False),
        Attribute('search_algorithm', is_required=False),
        Attribute('has_early_stopping', attr_type=bool, is_required=False),
        Attribute('has_description', attr_type=bool),
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
        Attribute('concurrency', is_required=False),
        Attribute('search_algorithm', is_required=False),
        Attribute('has_early_stopping', attr_type=bool, is_required=False),
        Attribute('has_description', attr_type=bool),
        Attribute('last_status'),
    )


class ExperimentGroupStoppedEvent(Event):
    event_type = EXPERIMENT_GROUP_STOPPED
    attributes = (
        Attribute('id'),
        Attribute('sequence'),
        Attribute('project.id'),
        Attribute('project.user.id'),
        Attribute('user.id'),
        Attribute('updated_at', is_datetime=True),
        Attribute('concurrency', is_required=False),
        Attribute('search_algorithm', is_required=False),
        Attribute('has_early_stopping', attr_type=bool, is_required=False),
        Attribute('has_description', attr_type=bool),
        Attribute('last_status'),
        Attribute('previous_status', is_required=False),
    )


class ExperimentGroupResumedEvent(Event):
    event_type = EXPERIMENT_GROUP_RESUMED
    attributes = (
        Attribute('id'),
        Attribute('sequence'),
        Attribute('project.id'),
        Attribute('project.user.id'),
        Attribute('user.id'),
        Attribute('updated_at', is_datetime=True),
        Attribute('concurrency', is_required=False),
        Attribute('search_algorithm', is_required=False),
        Attribute('has_early_stopping', attr_type=bool, is_required=False),
        Attribute('has_description', attr_type=bool),
        Attribute('last_status'),
    )


class ExperimentGroupDoneEvent(Event):
    event_type = EXPERIMENT_GROUP_DONE
    attributes = (
        Attribute('id'),
        Attribute('sequence'),
        Attribute('project.id'),
        Attribute('project.user.id'),
        Attribute('user.id'),
        Attribute('updated_at', is_datetime=True),
        Attribute('concurrency', is_required=False),
        Attribute('search_algorithm', is_required=False),
        Attribute('has_early_stopping', attr_type=bool, is_required=False),
        Attribute('has_description', attr_type=bool),
        Attribute('last_status'),
        Attribute('previous_status', is_required=False),
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
        Attribute('concurrency', is_required=False),
        Attribute('search_algorithm', is_required=False),
        Attribute('has_early_stopping', attr_type=bool, is_required=False),
        Attribute('has_description', attr_type=bool),
        Attribute('last_status'),
        Attribute('previous_status', is_required=False),
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
        Attribute('concurrency', is_required=False),
        Attribute('search_algorithm', is_required=False),
        Attribute('has_early_stopping', attr_type=bool, is_required=False),
        Attribute('has_description', attr_type=bool),
        Attribute('last_status'),
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
        Attribute('concurrency', is_required=False),
        Attribute('search_algorithm', is_required=False),
        Attribute('has_early_stopping', attr_type=bool, is_required=False),
        Attribute('has_description', attr_type=bool),
        Attribute('last_status'),
    )


class ExperimentGroupRandomEvent(Event):
    event_type = EXPERIMENT_GROUP_RANDOM


class ExperimentGroupGridEvent(Event):
    event_type = EXPERIMENT_GROUP_GRID


class ExperimentGroupHyperbandEvent(Event):
    event_type = EXPERIMENT_GROUP_HYPERBAND


class ExperimentGroupBOEvent(Event):
    event_type = EXPERIMENT_GROUP_BO


class ExperimentGroupDeletedTriggeredEvent(Event):
    event_type = EXPERIMENT_GROUP_DELETED_TRIGGERED
    actor_id = 'actor_id'
    attributes = (
        Attribute('id'),
        Attribute('sequence'),
        Attribute('project.id'),
        Attribute('project.user.id'),
        Attribute('user.id'),
        Attribute('actor_id'),
        Attribute('updated_at', is_datetime=True),
        Attribute('concurrency', is_required=False),
        Attribute('search_algorithm', is_required=False),
        Attribute('has_early_stopping', attr_type=bool, is_required=False),
        Attribute('has_description', attr_type=bool),
        Attribute('last_status'),
    )


class ExperimentGroupStoppedTriggeredEvent(Event):
    event_type = EXPERIMENT_GROUP_STOPPED_TRIGGERED
    actor_id = 'actor_id'
    attributes = (
        Attribute('id'),
        Attribute('sequence'),
        Attribute('project.id'),
        Attribute('project.user.id'),
        Attribute('user.id'),
        Attribute('actor_id'),
        Attribute('updated_at', is_datetime=True),
        Attribute('concurrency', is_required=False),
        Attribute('search_algorithm', is_required=False),
        Attribute('has_early_stopping', attr_type=bool, is_required=False),
        Attribute('has_description', attr_type=bool),
        Attribute('last_status'),
        Attribute('pending', attr_type=bool, is_required=False),
    )


class ExperimentGroupResumedTriggeredEvent(Event):
    event_type = EXPERIMENT_GROUP_RESUMED_TRIGGERED
    actor_id = 'actor_id'
    attributes = (
        Attribute('id'),
        Attribute('sequence'),
        Attribute('project.id'),
        Attribute('project.user.id'),
        Attribute('user.id'),
        Attribute('actor_id'),
        Attribute('updated_at', is_datetime=True),
        Attribute('concurrency', is_required=False),
        Attribute('search_algorithm', is_required=False),
        Attribute('has_early_stopping', attr_type=bool, is_required=False),
        Attribute('has_description', attr_type=bool),
        Attribute('last_status'),
    )
