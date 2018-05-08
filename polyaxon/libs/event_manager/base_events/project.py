from libs.event_manager.event import Event

PROJECT_CREATED = 'project.created'
PROJECT_UPDATED = 'project.updated'
PROJECT_SET_PUBLIC = 'project.set_public'  # params same user, other user, access granted
PROJECT_SET_PRIVATE = 'project.set_private'  # params same user, other user, access granted
PROJECT_DELETED = 'project.deleted'  # params same user, other user, access granted
PROJECT_VIEWED = 'project.viewed'  # params same user, other user, access granted
PROJECT_EXPERIMENTS_VIEWED = 'project.experiments_viewed'
PROJECT_EXPERIMENT_GROUPS_VIEWED = 'project.experiment_groups_viewed'


class ProjectCreatedEvent(Event):
    type = PROJECT_CREATED


class ProjectUpdatedEvent(Event):
    type = PROJECT_UPDATED


class ProjectDeletedEvent(Event):
    type = PROJECT_DELETED


class ProjectViewedEvent(Event):
    type = PROJECT_VIEWED


class ProjectSetPublicEvent(Event):
    type = PROJECT_SET_PUBLIC


class ProjectSetPrivateEvent(Event):
    type = PROJECT_SET_PRIVATE


class ProjectExperimentsViewedEvent(Event):
    type = PROJECT_EXPERIMENTS_VIEWED


class ProjectExperimentGroupsViewedEvent(Event):
    type = PROJECT_EXPERIMENT_GROUPS_VIEWED
