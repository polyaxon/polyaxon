import analytics
from event_manager.events import project

analytics.register(project.ProjectCreatedEvent)
analytics.register(project.ProjectUpdatedEvent)
analytics.register(project.ProjectDeletedEvent)
analytics.register(project.ProjectViewedEvent)
analytics.register(project.ProjectSetPublicEvent)
analytics.register(project.ProjectSetPrivateEvent)
analytics.register(project.ProjectExperimentsViewedEvent)
analytics.register(project.ProjectExperimentGroupsViewedEvent)

