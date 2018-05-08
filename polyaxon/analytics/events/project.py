import analytics
from libs.event_manager.base_events import project

analytics.register(project.ProjectCreatedEvent)
analytics.register(project.ProjectUpdatedEvent)
analytics.register(project.ProjectDeletedEvent)
analytics.register(project.ProjectViewedEvent)
analytics.register(project.ProjectSetPublicEvent)
analytics.register(project.ProjectSetPrivateEvent)
analytics.register(project.ProjectExperimentsViewedEvent)
analytics.register(project.ProjectExperimentGroupsViewedEvent)

