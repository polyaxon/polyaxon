from event_manager.event import Event, Attribute

PROJECT_CREATED = 'project.created'
PROJECT_UPDATED = 'project.updated'
PROJECT_SET_PUBLIC = 'project.set_public'
PROJECT_SET_PRIVATE = 'project.set_private'
PROJECT_DELETED = 'project.deleted'
PROJECT_VIEWED = 'project.viewed'
PROJECT_EXPERIMENTS_VIEWED = 'project.experiments_viewed'
PROJECT_EXPERIMENT_GROUPS_VIEWED = 'project.experiment_groups_viewed'


class ProjectCreatedEvent(Event):
    type = PROJECT_CREATED
    attributes = (
        Attribute('id'),
        Attribute('user.id'),
        Attribute('created_at', is_datetime=True),
        Attribute('has_description', attr_type=bool),
        Attribute('is_public', attr_type=bool),
    )


class ProjectUpdatedEvent(Event):
    type = PROJECT_UPDATED
    attributes = (
        Attribute('id'),
        Attribute('user.id'),
        Attribute('actor_id'),
        Attribute('updated_at', is_datetime=True),
        Attribute('has_description', attr_type=bool),
        Attribute('is_public', attr_type=bool),
    )


class ProjectDeletedEvent(Event):
    type = PROJECT_DELETED
    attributes = (
        Attribute('id'),
        Attribute('user.id'),
        Attribute('actor_id'),
        Attribute('is_public', attr_type=bool),
    )


class ProjectViewedEvent(Event):
    type = PROJECT_VIEWED
    attributes = (
        Attribute('id'),
        Attribute('user.id'),
        Attribute('actor_id'),
        Attribute('is_public', attr_type=bool),
    )


class ProjectSetPublicEvent(Event):
    type = PROJECT_SET_PUBLIC
    attributes = (
        Attribute('id'),
        Attribute('user.id'),
        Attribute('actor_id'),
    )


class ProjectSetPrivateEvent(Event):
    type = PROJECT_SET_PRIVATE
    attributes = (
        Attribute('id'),
        Attribute('user.id'),
        Attribute('actor_id'),
    )


class ProjectExperimentsViewedEvent(Event):
    type = PROJECT_EXPERIMENTS_VIEWED
    attributes = (
        Attribute('id'),
        Attribute('user.id'),
        Attribute('actor_id'),
        Attribute('is_public', attr_type=bool),
    )


class ProjectExperimentGroupsViewedEvent(Event):
    type = PROJECT_EXPERIMENT_GROUPS_VIEWED
    attributes = (
        Attribute('id'),
        Attribute('user.id'),
        Attribute('actor_id'),
        Attribute('is_public', attr_type=bool),
    )
