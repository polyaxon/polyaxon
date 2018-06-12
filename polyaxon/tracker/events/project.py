import tracker

from event_manager.events import project

tracker.subscribe(project.ProjectCreatedEvent)
tracker.subscribe(project.ProjectUpdatedEvent)
tracker.subscribe(project.ProjectDeletedEvent)
tracker.subscribe(project.ProjectDeletedTriggeredEvent)
tracker.subscribe(project.ProjectViewedEvent)
tracker.subscribe(project.ProjectSetPublicEvent)
tracker.subscribe(project.ProjectSetPrivateEvent)
tracker.subscribe(project.ProjectExperimentsViewedEvent)
tracker.subscribe(project.ProjectExperimentGroupsViewedEvent)
tracker.subscribe(project.ProjectJobsViewedEvent)
