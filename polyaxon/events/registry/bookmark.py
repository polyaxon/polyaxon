from events import event_actions, event_subjects
from events.event import Attribute, Event

BOOKMARK_BUILD_JOBS_VIEWED = '{}.{}'.format(event_subjects.BOOKMARK,
                                            event_actions.BUILDS_VIEWED)
BOOKMARK_JOBS_VIEWED = '{}.{}'.format(event_subjects.BOOKMARK,
                                      event_actions.JOBS_VIEWED)
BOOKMARK_EXPERIMENTS_VIEWED = '{}.{}'.format(event_subjects.BOOKMARK,
                                             event_actions.EXPERIMENTS_VIEWED)
BOOKMARK_EXPERIMENT_GROUPS_VIEWED = '{}.{}'.format(event_subjects.BOOKMARK,
                                                   event_actions.EXPERIMENT_GROUPS_VIEWED)
BOOKMARK_PROJECTS_VIEWED = '{}.{}'.format(event_subjects.BOOKMARK,
                                          event_actions.PROJECTS_VIEWED)

EVENTS = {
    BOOKMARK_BUILD_JOBS_VIEWED,
    BOOKMARK_JOBS_VIEWED,
    BOOKMARK_EXPERIMENTS_VIEWED,
    BOOKMARK_EXPERIMENT_GROUPS_VIEWED,
    BOOKMARK_PROJECTS_VIEWED,
}


class BookmarkBuildJobsViewedEvent(Event):
    event_type = BOOKMARK_BUILD_JOBS_VIEWED
    actor = True
    attributes = (
        Attribute('id'),
    )


class BookmarkJobsViewedEvent(Event):
    event_type = BOOKMARK_JOBS_VIEWED
    actor = True
    attributes = (
        Attribute('id'),
    )


class BookmarkExperimentsViewedEvent(Event):
    event_type = BOOKMARK_EXPERIMENTS_VIEWED
    actor = True
    attributes = (
        Attribute('id'),
    )


class BookmarkExperimentGroupsViewedEvent(Event):
    event_type = BOOKMARK_EXPERIMENT_GROUPS_VIEWED
    actor = True
    attributes = (
        Attribute('id'),
    )


class BookmarkProjectsViewedEvent(Event):
    event_type = BOOKMARK_PROJECTS_VIEWED
    actor = True
    attributes = (
        Attribute('id'),
    )
