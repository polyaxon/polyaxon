import analytics
from event_manager.events import project

analytics.subscribe(project.ProjectCreatedEvent)
analytics.subscribe(project.ProjectUpdatedEvent)
analytics.subscribe(project.ProjectDeletedEvent)
analytics.subscribe(project.ProjectViewedEvent)
analytics.subscribe(project.ProjectSetPublicEvent)
analytics.subscribe(project.ProjectSetPrivateEvent)
analytics.subscribe(project.ProjectExperimentsViewedEvent)
analytics.subscribe(project.ProjectExperimentGroupsViewedEvent)

