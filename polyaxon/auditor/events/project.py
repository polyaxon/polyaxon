import auditor

from event_manager.events import project

auditor.subscribe(project.ProjectCreatedEvent)
auditor.subscribe(project.ProjectUpdatedEvent)
auditor.subscribe(project.ProjectDeletedEvent)
auditor.subscribe(project.ProjectDeletedTriggeredEvent)
auditor.subscribe(project.ProjectViewedEvent)
auditor.subscribe(project.ProjectSetPublicEvent)
auditor.subscribe(project.ProjectSetPrivateEvent)
auditor.subscribe(project.ProjectExperimentsViewedEvent)
auditor.subscribe(project.ProjectExperimentGroupsViewedEvent)
auditor.subscribe(project.ProjectJobsViewedEvent)
auditor.subscribe(project.ProjectBuildsViewedEvent)
auditor.subscribe(project.ProjectTensorboardsViewedEvent)
