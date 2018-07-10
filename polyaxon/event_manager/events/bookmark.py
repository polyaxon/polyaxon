from event_manager import event_actions, event_subjects
from event_manager.event import Attribute, Event

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


class BookmarkBuildJobsViewedEvent(Event):
    event_type = BOOKMARK_BUILD_JOBS_VIEWED
    actor_id = 'actor_id'
    attributes = (
        Attribute('actor_id'),
        Attribute('id'),
    )


class BookmarkJobsViewedEvent(Event):
    event_type = BOOKMARK_JOBS_VIEWED
    actor_id = 'actor_id'
    attributes = (
        Attribute('actor_id'),
        Attribute('id'),
    )


class BookmarkExperimentsViewedEvent(Event):
    event_type = BOOKMARK_EXPERIMENTS_VIEWED
    actor_id = 'actor_id'
    attributes = (
        Attribute('actor_id'),
        Attribute('id'),
    )


class BookmarkExperimentGroupsViewedEvent(Event):
    event_type = BOOKMARK_EXPERIMENT_GROUPS_VIEWED
    actor_id = 'actor_id'
    attributes = (
        Attribute('actor_id'),
        Attribute('id'),
    )


class BookmarkProjectsViewedEvent(Event):
    event_type = BOOKMARK_PROJECTS_VIEWED
    actor_id = 'actor_id'
    attributes = (
        Attribute('actor_id'),
        Attribute('id'),
    )
