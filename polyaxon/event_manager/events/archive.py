from event_manager import event_actions, event_subjects
from event_manager.event import Attribute, Event

ARCHIVE_BUILD_JOBS_VIEWED = '{}.{}'.format(event_subjects.ARCHIVE,
                                           event_actions.BUILDS_VIEWED)
ARCHIVE_JOBS_VIEWED = '{}.{}'.format(event_subjects.ARCHIVE,
                                     event_actions.JOBS_VIEWED)
ARCHIVE_EXPERIMENTS_VIEWED = '{}.{}'.format(event_subjects.ARCHIVE,
                                            event_actions.EXPERIMENTS_VIEWED)
ARCHIVE_EXPERIMENT_GROUPS_VIEWED = '{}.{}'.format(event_subjects.ARCHIVE,
                                                  event_actions.EXPERIMENT_GROUPS_VIEWED)
ARCHIVE_PROJECTS_VIEWED = '{}.{}'.format(event_subjects.ARCHIVE,
                                         event_actions.PROJECTS_VIEWED)


class ArchiveBuildJobsViewedEvent(Event):
    event_type = ARCHIVE_BUILD_JOBS_VIEWED
    actor = True
    attributes = (
        Attribute('id'),
    )


class ArchiveJobsViewedEvent(Event):
    event_type = ARCHIVE_JOBS_VIEWED
    actor = True
    attributes = (
        Attribute('id'),
    )


class ArchiveExperimentsViewedEvent(Event):
    event_type = ARCHIVE_EXPERIMENTS_VIEWED
    actor = True
    attributes = (
        Attribute('id'),
    )


class ArchiveExperimentGroupsViewedEvent(Event):
    event_type = ARCHIVE_EXPERIMENT_GROUPS_VIEWED
    actor = True
    attributes = (
        Attribute('id'),
    )


class ArchiveProjectsViewedEvent(Event):
    event_type = ARCHIVE_PROJECTS_VIEWED
    actor = True
    attributes = (
        Attribute('id'),
    )
