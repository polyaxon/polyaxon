from event_manager import event_actions, event_subjects
from event_manager.event import Attribute, Event

PROJECT_CREATED = '{}.{}'.format(event_subjects.PROJECT, event_actions.CREATED)
PROJECT_UPDATED = '{}.{}'.format(event_subjects.PROJECT, event_actions.UPDATED)
PROJECT_DELETED = '{}.{}'.format(event_subjects.PROJECT, event_actions.DELETED)
PROJECT_VIEWED = '{}.{}'.format(event_subjects.PROJECT, event_actions.VIEWED)
PROJECT_SET_PUBLIC = '{}.set_public'.format(event_subjects.PROJECT)
PROJECT_SET_PRIVATE = '{}.set_private'.format(event_subjects.PROJECT)
PROJECT_EXPERIMENTS_VIEWED = '{}.{}'.format(event_subjects.PROJECT,
                                            event_actions.EXPERIMENTS_VIEWED)
PROJECT_EXPERIMENT_GROUPS_VIEWED = '{}.{}'.format(event_subjects.PROJECT,
                                                  event_actions.EXPERIMENT_GROUPS_VIEWED)


class ProjectCreatedEvent(Event):
    event_type = PROJECT_CREATED
    actor_id = 'user.id'
    attributes = (
        Attribute('id'),
        Attribute('user.id'),
        Attribute('created_at', is_datetime=True),
        Attribute('has_description', attr_type=bool),
        Attribute('is_public', attr_type=bool),
    )


class ProjectUpdatedEvent(Event):
    event_type = PROJECT_UPDATED
    actor_id = 'actor_id'
    attributes = (
        Attribute('id'),
        Attribute('user.id'),
        Attribute('actor_id'),
        Attribute('updated_at', is_datetime=True),
        Attribute('has_description', attr_type=bool),
        Attribute('is_public', attr_type=bool),
    )


class ProjectDeletedEvent(Event):
    event_type = PROJECT_DELETED
    actor_id = 'actor_id'
    attributes = (
        Attribute('id'),
        Attribute('user.id'),
        Attribute('actor_id'),
        Attribute('is_public', attr_type=bool),
    )


class ProjectViewedEvent(Event):
    event_type = PROJECT_VIEWED
    actor_id = 'actor_id'
    attributes = (
        Attribute('id'),
        Attribute('user.id'),
        Attribute('actor_id'),
        Attribute('is_public', attr_type=bool),
    )


class ProjectSetPublicEvent(Event):
    event_type = PROJECT_SET_PUBLIC
    actor_id = 'actor_id'
    attributes = (
        Attribute('id'),
        Attribute('user.id'),
        Attribute('actor_id'),
    )


class ProjectSetPrivateEvent(Event):
    event_type = PROJECT_SET_PRIVATE
    actor_id = 'actor_id'
    attributes = (
        Attribute('id'),
        Attribute('user.id'),
        Attribute('actor_id'),
    )


class ProjectExperimentsViewedEvent(Event):
    event_type = PROJECT_EXPERIMENTS_VIEWED
    actor_id = 'actor_id'
    attributes = (
        Attribute('id'),
        Attribute('user.id'),
        Attribute('actor_id'),
        Attribute('is_public', attr_type=bool),
    )


class ProjectExperimentGroupsViewedEvent(Event):
    event_type = PROJECT_EXPERIMENT_GROUPS_VIEWED
    actor_id = 'actor_id'
    attributes = (
        Attribute('id'),
        Attribute('user.id'),
        Attribute('actor_id'),
        Attribute('is_public', attr_type=bool),
    )
