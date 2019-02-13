import auditor

from event_manager.events import archive

auditor.subscribe(archive.ArchiveBuildJobsViewedEvent)
auditor.subscribe(archive.ArchiveJobsViewedEvent)
auditor.subscribe(archive.ArchiveExperimentsViewedEvent)
auditor.subscribe(archive.ArchiveExperimentGroupsViewedEvent)
auditor.subscribe(archive.ArchiveProjectsViewedEvent)
