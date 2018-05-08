import auditor
from event_manager.events import project

auditor.register(project.ProjectCreatedEvent)
auditor.register(project.ProjectUpdatedEvent)
auditor.register(project.ProjectDeletedEvent)
auditor.register(project.ProjectViewedEvent)
auditor.register(project.ProjectSetPublicEvent)
auditor.register(project.ProjectSetPrivateEvent)
auditor.register(project.ProjectExperimentsViewedEvent)
auditor.register(project.ProjectExperimentGroupsViewedEvent)
