from event_manager import event_actions, event_subjects
from event_manager.event import Attribute, Event

PIPELINE_RUN_CREATED = '{}.{}'.format(event_subjects.PIPELINE_RUN,
                                      event_actions.CREATED)
PIPELINE_RUN_UPDATED = '{}.{}'.format(event_subjects.PIPELINE_RUN,
                                      event_actions.UPDATED)
PIPELINE_RUN_DELETED = '{}.{}'.format(event_subjects.PIPELINE_RUN,
                                      event_actions.DELETED)
PIPELINE_RUN_VIEWED = '{}.{}'.format(event_subjects.PIPELINE_RUN,
                                     event_actions.VIEWED)
PIPELINE_RUN_ARCHIVED = '{}.{}'.format(event_subjects.PIPELINE_RUN,
                                       event_actions.ARCHIVED)
PIPELINE_RUN_RESTORED = '{}.{}'.format(event_subjects.PIPELINE_RUN,
                                       event_actions.RESTORED)
PIPELINE_RUN_STOPPED = '{}.{}'.format(event_subjects.PIPELINE_RUN,
                                      event_actions.STOPPED)
PIPELINE_RUN_SKIPPED = '{}.{}'.format(event_subjects.PIPELINE_RUN,
                                      event_actions.SKIPPED)
PIPELINE_RUN_RESUMED = '{}.{}'.format(event_subjects.PIPELINE_RUN,
                                      event_actions.RESUMED)
PIPELINE_RUN_RESTARTED = '{}.{}'.format(event_subjects.PIPELINE_RUN,
                                        event_actions.RESTARTED)
PIPELINE_RUN_NEW_STATUS = '{}.{}'.format(event_subjects.PIPELINE_RUN,
                                         event_actions.NEW_STATUS)
PIPELINE_RUN_SUCCEEDED = '{}.{}'.format(event_subjects.PIPELINE_RUN,
                                        event_actions.SUCCEEDED)
PIPELINE_RUN_FAILED = '{}.{}'.format(event_subjects.PIPELINE_RUN,
                                     event_actions.FAILED)
PIPELINE_RUN_DONE = '{}.{}'.format(event_subjects.PIPELINE_RUN,
                                   event_actions.DONE)
PIPELINE_RUN_DELETED_TRIGGERED = '{}.{}.{}'.format(event_subjects.PIPELINE_RUN,
                                                   event_actions.DELETED,
                                                   event_subjects.TRIGGER)
PIPELINE_RUN_CLEANED_TRIGGERED = '{}.{}.{}'.format(event_subjects.PIPELINE_RUN,
                                                   event_actions.CLEANED,
                                                   event_subjects.TRIGGER)
PIPELINE_RUN_STOPPED_TRIGGERED = '{}.{}.{}'.format(event_subjects.PIPELINE_RUN,
                                                   event_actions.STOPPED,
                                                   event_subjects.TRIGGER)
PIPELINE_RUN_RESUMED_TRIGGERED = '{}.{}.{}'.format(event_subjects.PIPELINE_RUN,
                                                   event_actions.RESUMED,
                                                   event_subjects.TRIGGER)
PIPELINE_RUN_RESTARTED_TRIGGERED = '{}.{}.{}'.format(event_subjects.PIPELINE_RUN,
                                                     event_actions.RESTARTED,
                                                     event_subjects.TRIGGER)
PIPELINE_RUN_SKIPPED_TRIGGERED = '{}.{}.{}'.format(event_subjects.PIPELINE_RUN,
                                                   event_actions.SKIPPED,
                                                   event_subjects.TRIGGER)

EVENTS = {
    PIPELINE_RUN_CREATED,
    PIPELINE_RUN_UPDATED,
    PIPELINE_RUN_DELETED,
    PIPELINE_RUN_VIEWED,
    PIPELINE_RUN_ARCHIVED,
    PIPELINE_RUN_RESTORED,
    PIPELINE_RUN_STOPPED,
    PIPELINE_RUN_SKIPPED,
    PIPELINE_RUN_RESUMED,
    PIPELINE_RUN_RESTARTED,
    PIPELINE_RUN_NEW_STATUS,
    PIPELINE_RUN_SUCCEEDED,
    PIPELINE_RUN_FAILED,
    PIPELINE_RUN_DONE,
    PIPELINE_RUN_DELETED_TRIGGERED,
    PIPELINE_RUN_CLEANED_TRIGGERED,
    PIPELINE_RUN_STOPPED_TRIGGERED,
    PIPELINE_RUN_RESUMED_TRIGGERED,
    PIPELINE_RUN_RESTARTED_TRIGGERED,
    PIPELINE_RUN_SKIPPED_TRIGGERED,
}


class PipelineRunCreatedEvent(Event):
    event_type = PIPELINE_RUN_CREATED
    actor = True
    attributes = (
        Attribute('id'),
        Attribute('pipeline.id'),
        Attribute('created_at', is_datetime=True),
    )


class PipelineRunUpdatedEvent(Event):
    event_type = PIPELINE_RUN_UPDATED
    actor = True
    attributes = (
        Attribute('id'),
        Attribute('pipeline.id'),
        Attribute('updated_at', is_datetime=True),
    )


class PipelineRunDeletedEvent(Event):
    event_type = PIPELINE_RUN_DELETED
    attributes = (
        Attribute('id'),
    )


class PipelineRunViewedEvent(Event):
    event_type = PIPELINE_RUN_VIEWED
    actor = True
    attributes = (
        Attribute('id'),
        Attribute('pipeline.id'),
    )


class PipelineRunArchivedEvent(Event):
    event_type = PIPELINE_RUN_ARCHIVED
    actor = True
    attributes = (
        Attribute('id'),
        Attribute('pipeline.id'),
    )


class PipelineRunRestoredEvent(Event):
    event_type = PIPELINE_RUN_RESTORED
    actor = True
    attributes = (
        Attribute('id'),
        Attribute('pipeline.id'),
        Attribute('last_status'),
    )


class PipelineRunStoppedEvent(Event):
    event_type = PIPELINE_RUN_STOPPED
    attributes = (
        Attribute('id'),
        Attribute('pipeline.id'),
        Attribute('last_status'),
        Attribute('previous_status', is_required=False),
    )


class PipelineRunSkippedEvent(Event):
    event_type = PIPELINE_RUN_SKIPPED
    attributes = (
        Attribute('id'),
        Attribute('pipeline.id'),
        Attribute('last_status'),
        Attribute('previous_status', is_required=False),
    )


class PipelineRunResumedEvent(Event):
    event_type = PIPELINE_RUN_RESUMED
    attributes = (
        Attribute('id'),
        Attribute('pipeline.id'),
        Attribute('last_status'),
        Attribute('previous_status', is_required=False),
    )


class PipelineRunRestartedEvent(Event):
    event_type = PIPELINE_RUN_RESTARTED
    attributes = (
        Attribute('id'),
        Attribute('pipeline.id'),
        Attribute('last_status'),
    )


class PipelineRunNewStatusEvent(Event):
    event_type = PIPELINE_RUN_NEW_STATUS
    attributes = (
        Attribute('id'),
        Attribute('pipeline.id'),
        Attribute('last_status'),
        Attribute('previous_status', is_required=False),
    )


class PipelineRunSucceededEvent(Event):
    event_type = PIPELINE_RUN_SUCCEEDED
    attributes = (
        Attribute('id'),
        Attribute('pipeline.id'),
        Attribute('previous_status', is_required=False),
    )


class PipelineRunFailedEvent(Event):
    event_type = PIPELINE_RUN_FAILED
    attributes = (
        Attribute('id'),
        Attribute('pipeline.id'),
        Attribute('last_status'),
        Attribute('previous_status', is_required=False),
    )


class PipelineRunDoneEvent(Event):
    event_type = PIPELINE_RUN_DONE
    attributes = (
        Attribute('id'),
        Attribute('pipeline.id'),
        Attribute('last_status'),
        Attribute('previous_status', is_required=False),
    )


class PipelineRunDeletedTriggeredEvent(Event):
    event_type = PIPELINE_RUN_DELETED_TRIGGERED
    actor = True
    attributes = (
        Attribute('id'),
        Attribute('pipeline.id'),
        Attribute('last_status'),
    )


class PipelineRunCleanedTriggeredEvent(Event):
    event_type = PIPELINE_RUN_CLEANED_TRIGGERED
    attributes = (
        Attribute('id'),
    )


class PipelineRunStoppedTriggeredEvent(Event):
    event_type = PIPELINE_RUN_STOPPED_TRIGGERED
    actor = True
    attributes = (
        Attribute('id'),
        Attribute('pipeline.id'),
        Attribute('last_status'),
    )


class PipelineRunResumedTriggeredEvent(Event):
    event_type = PIPELINE_RUN_RESUMED_TRIGGERED
    actor = True
    attributes = (
        Attribute('id'),
        Attribute('pipeline.id'),
        Attribute('last_status'),
    )


class PipelineRunRestartedTriggeredEvent(Event):
    event_type = PIPELINE_RUN_RESTARTED_TRIGGERED
    actor = True
    attributes = (
        Attribute('id'),
        Attribute('pipeline.id'),
        Attribute('last_status'),
    )


class PipelineRunSkippedTriggeredEvent(Event):
    event_type = PIPELINE_RUN_SKIPPED_TRIGGERED
    actor = True
    attributes = (
        Attribute('id'),
        Attribute('pipeline.id'),
        Attribute('last_status'),
    )
