import tracker

from event_manager.events import archive

tracker.subscribe(archive.ArchiveBuildJobsViewedEvent)
tracker.subscribe(archive.ArchiveJobsViewedEvent)
tracker.subscribe(archive.ArchiveExperimentsViewedEvent)
tracker.subscribe(archive.ArchiveExperimentGroupsViewedEvent)
tracker.subscribe(archive.ArchiveProjectsViewedEvent)
