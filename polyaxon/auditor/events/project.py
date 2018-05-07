import auditor
from libs.event_manager import event_types
from libs.event_manager.event import Event


class ProjectCreatedEvent(Event):
    type = event_types.PROJECT_CREATED


class ProjectUpdatedEvent(Event):
    type = event_types.PROJECT_UPDATED


class ProjectDeletedEvent(Event):
    type = event_types.PROJECT_DELETED


class ProjectViewedEvent(Event):
    type = event_types.PROJECT_VIEWED


class ProjectSetPublicEvent(Event):
    type = event_types.PROJECT_SET_PUBLIC


class ProjectSetPrivateEvent(Event):
    type = event_types.PROJECT_SET_PRIVATE


class ProjectExperimentsViewedEvent(Event):
    type = event_types.PROJECT_EXPERIMENTS_VIEWED


class ProjectExperimentGroupsViewedEvent(Event):
    type = event_types.PROJECT_EXPERIMENT_GROUPS_VIEWED


auditor.register(ProjectCreatedEvent)
auditor.register(ProjectUpdatedEvent)
auditor.register(ProjectDeletedEvent)
auditor.register(ProjectViewedEvent)
auditor.register(ProjectSetPublicEvent)
auditor.register(ProjectSetPrivateEvent)
auditor.register(ProjectExperimentsViewedEvent)
auditor.register(ProjectExperimentGroupsViewedEvent)

