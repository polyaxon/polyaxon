from event_manager import event_actions, event_subjects
from event_manager.event import Attribute, Event

BUILD_JOB_STARTED = '{}.{}'.format(event_subjects.BUILD_JOB, event_actions.STARTED)
BUILD_JOB_STARTED_TRIGGERED = '{}.{}.{}'.format(event_subjects.BUILD_JOB,
                                                event_actions.STARTED,
                                                event_subjects.TRIGGER)
BUILD_JOB_STOPPED = '{}.{}'.format(event_subjects.BUILD_JOB, event_actions.STOPPED)
BUILD_JOB_STOPPED_TRIGGERED = '{}.{}.{}'.format(event_subjects.BUILD_JOB,
                                                event_actions.STOPPED,
                                                event_subjects.TRIGGER)
BUILD_JOB_CLEANED_TRIGGERED = '{}.{}.{}'.format(event_subjects.BUILD_JOB,
                                                event_actions.CLEANED,
                                                event_subjects.TRIGGER)
BUILD_JOB_CREATED = '{}.{}'.format(event_subjects.BUILD_JOB, event_actions.CREATED)
BUILD_JOB_VIEWED = '{}.{}'.format(event_subjects.BUILD_JOB, event_actions.VIEWED)
BUILD_JOB_ARCHIVED = '{}.{}'.format(event_subjects.BUILD_JOB, event_actions.ARCHIVED)
BUILD_JOB_RESTORED = '{}.{}'.format(event_subjects.BUILD_JOB, event_actions.RESTORED)
BUILD_JOB_BOOKMARKED = '{}.{}'.format(event_subjects.BUILD_JOB, event_actions.BOOKMARKED)
BUILD_JOB_UNBOOKMARKED = '{}.{}'.format(event_subjects.BUILD_JOB, event_actions.UNBOOKMARKED)
BUILD_JOB_UPDATED = '{}.{}'.format(event_subjects.BUILD_JOB, event_actions.UPDATED)
BUILD_JOB_NEW_STATUS = '{}.{}'.format(event_subjects.BUILD_JOB, event_actions.NEW_STATUS)
BUILD_JOB_FAILED = '{}.{}'.format(event_subjects.BUILD_JOB, event_actions.FAILED)
BUILD_JOB_SUCCEEDED = '{}.{}'.format(event_subjects.BUILD_JOB, event_actions.SUCCEEDED)
BUILD_JOB_DONE = '{}.{}'.format(event_subjects.BUILD_JOB, event_actions.DONE)
BUILD_JOB_DELETED = '{}.{}'.format(event_subjects.BUILD_JOB, event_actions.DELETED)
BUILD_JOB_DELETED_TRIGGERED = '{}.{}.{}'.format(event_subjects.BUILD_JOB,
                                                event_actions.DELETED,
                                                event_subjects.TRIGGER)
BUILD_JOB_LOGS_VIEWED = '{}.{}'.format(event_subjects.BUILD_JOB, event_actions.LOGS_VIEWED)
BUILD_JOB_STATUSES_VIEWED = '{}.{}'.format(event_subjects.BUILD_JOB,
                                           event_actions.STATUSES_VIEWED)


class BuildJobCreatedEvent(Event):
    event_type = BUILD_JOB_CREATED
    actor = True
    actor_id = 'user.id'
    actor_name = 'user.username'
    attributes = (
        Attribute('id'),
        Attribute('project.id'),
        Attribute('project.user.id'),
        Attribute('created_at', is_datetime=True),
        Attribute('has_specification', attr_type=bool),
        Attribute('has_description', attr_type=bool),
    )


class BuildJobUpdatedEvent(Event):
    event_type = BUILD_JOB_UPDATED
    actor = True
    attributes = (
        Attribute('id'),
        Attribute('project.id'),
        Attribute('project.user.id'),
        Attribute('created_at', is_datetime=True),
        Attribute('has_description', attr_type=bool),
    )


class BuildJobStartedEvent(Event):
    event_type = BUILD_JOB_STARTED
    attributes = (
        Attribute('id'),
        Attribute('user.id'),
        Attribute('project.id'),
        Attribute('project.user.id'),
    )


class BuildJobStartedTriggeredEvent(Event):
    event_type = BUILD_JOB_STARTED_TRIGGERED
    actor = True
    attributes = (
        Attribute('id'),
        Attribute('user.id'),
        Attribute('project.id'),
        Attribute('project.user.id'),
    )


class BuildJobSoppedEvent(Event):
    event_type = BUILD_JOB_STOPPED
    attributes = (
        Attribute('id'),
        Attribute('user.id'),
        Attribute('project.id'),
        Attribute('project.user.id'),
        Attribute('last_status'),
        Attribute('previous_status', is_required=False),
    )


class BuildJobSoppedTriggeredEvent(Event):
    event_type = BUILD_JOB_STOPPED_TRIGGERED
    actor = True
    attributes = (
        Attribute('id'),
        Attribute('user.id'),
        Attribute('project.id'),
        Attribute('project.user.id'),
        Attribute('last_status'),
    )


class BuildJobCleanedTriggeredEvent(Event):
    event_type = BUILD_JOB_CLEANED_TRIGGERED
    attributes = (
        Attribute('id'),
    )


class BuildJobViewedEvent(Event):
    event_type = BUILD_JOB_VIEWED
    actor = True
    attributes = (
        Attribute('id'),
        Attribute('user.id'),
        Attribute('project.id'),
        Attribute('project.user.id'),
        Attribute('last_status'),
    )


class BuildJobArchivedEvent(Event):
    event_type = BUILD_JOB_ARCHIVED
    actor = True
    attributes = (
        Attribute('id'),
        Attribute('user.id'),
        Attribute('project.id'),
        Attribute('project.user.id'),
        Attribute('last_status'),
    )


class BuildJobRestoredEvent(Event):
    event_type = BUILD_JOB_RESTORED
    actor = True
    attributes = (
        Attribute('id'),
        Attribute('user.id'),
        Attribute('project.id'),
        Attribute('project.user.id'),
        Attribute('last_status'),
    )


class BuildJobBookmarkedEvent(Event):
    event_type = BUILD_JOB_BOOKMARKED
    actor = True
    attributes = (
        Attribute('id'),
        Attribute('user.id'),
        Attribute('project.id'),
        Attribute('project.user.id'),
        Attribute('last_status'),
    )


class BuildJobUnBookmarkedEvent(Event):
    event_type = BUILD_JOB_UNBOOKMARKED
    actor = True
    attributes = (
        Attribute('id'),
        Attribute('user.id'),
        Attribute('project.id'),
        Attribute('project.user.id'),
        Attribute('last_status'),
    )


class BuildJobNewStatusEvent(Event):
    event_type = BUILD_JOB_NEW_STATUS
    attributes = (
        Attribute('id'),
        Attribute('user.id'),
        Attribute('project.id'),
        Attribute('last_status'),
    )


class BuildJobSucceededEvent(Event):
    event_type = BUILD_JOB_SUCCEEDED
    attributes = (
        Attribute('id'),
        Attribute('user.id'),
        Attribute('project.id'),
        Attribute('last_status'),
        Attribute('previous_status', is_required=False),
    )


class BuildJobDoneEvent(Event):
    event_type = BUILD_JOB_DONE
    attributes = (
        Attribute('id'),
        Attribute('user.id'),
        Attribute('project.id'),
        Attribute('last_status'),
        Attribute('previous_status', is_required=False),
    )


class BuildJobFailedEvent(Event):
    event_type = BUILD_JOB_FAILED
    attributes = (
        Attribute('id'),
        Attribute('user.id'),
        Attribute('project.id'),
        Attribute('last_status'),
        Attribute('previous_status', is_required=False),
    )


class BuildJobDeletedEvent(Event):
    event_type = BUILD_JOB_DELETED
    attributes = (
        Attribute('id'),
    )


class BuildJobDeletedTriggeredEvent(Event):
    event_type = BUILD_JOB_DELETED_TRIGGERED
    actor = True
    attributes = (
        Attribute('id'),
        Attribute('user.id'),
        Attribute('project.id'),
        Attribute('project.user.id'),
        Attribute('last_status'),
    )


class BuildJobLogsViewedEvent(Event):
    event_type = BUILD_JOB_LOGS_VIEWED
    actor = True
    attributes = (
        Attribute('id'),
        Attribute('project.id'),
        Attribute('project.user.id'),
        Attribute('user.id'),
        Attribute('has_description', attr_type=bool),
        Attribute('last_status'),
    )


class BuildJobStatusesViewedEvent(Event):
    event_type = BUILD_JOB_STATUSES_VIEWED
    actor = True
    attributes = (
        Attribute('id'),
        Attribute('project.id'),
        Attribute('project.user.id'),
        Attribute('user.id'),
        Attribute('last_status'),
    )
