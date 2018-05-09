from event_manager.event import Attribute, Event

PROJECT_CREATED = 'project.created'
PROJECT_UPDATED = 'project.updated'
PROJECT_DELETED = 'project.deleted'
PROJECT_VIEWED = 'project.viewed'
PROJECT_SET_PUBLIC = 'project.set_public'
PROJECT_SET_PRIVATE = 'project.set_private'
PROJECT_EXPERIMENTS_VIEWED = 'project.experiments_viewed'
PROJECT_EXPERIMENT_GROUPS_VIEWED = 'project.experiment_groups_viewed'


class ProjectCreatedEvent(Event):
    event_type = PROJECT_CREATED
    attributes = (
        Attribute('id'),
        Attribute('user.id'),
        Attribute('created_at', is_datetime=True),
        Attribute('has_description', attr_type=bool),
        Attribute('is_public', attr_type=bool),
    )


class ProjectUpdatedEvent(Event):
    event_type = PROJECT_UPDATED
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
    attributes = (
        Attribute('id'),
        Attribute('user.id'),
        Attribute('actor_id'),
        Attribute('is_public', attr_type=bool),
    )


class ProjectViewedEvent(Event):
    event_type = PROJECT_VIEWED
    attributes = (
        Attribute('id'),
        Attribute('user.id'),
        Attribute('actor_id'),
        Attribute('is_public', attr_type=bool),
    )


class ProjectSetPublicEvent(Event):
    event_type = PROJECT_SET_PUBLIC
    attributes = (
        Attribute('id'),
        Attribute('user.id'),
        Attribute('actor_id'),
    )


class ProjectSetPrivateEvent(Event):
    event_type = PROJECT_SET_PRIVATE
    attributes = (
        Attribute('id'),
        Attribute('user.id'),
        Attribute('actor_id'),
    )


class ProjectExperimentsViewedEvent(Event):
    event_type = PROJECT_EXPERIMENTS_VIEWED
    attributes = (
        Attribute('id'),
        Attribute('user.id'),
        Attribute('actor_id'),
        Attribute('is_public', attr_type=bool),
    )


class ProjectExperimentGroupsViewedEvent(Event):
    event_type = PROJECT_EXPERIMENT_GROUPS_VIEWED
    attributes = (
        Attribute('id'),
        Attribute('user.id'),
        Attribute('actor_id'),
        Attribute('is_public', attr_type=bool),
    )
