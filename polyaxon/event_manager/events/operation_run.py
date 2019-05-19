from event_manager import event_actions, event_subjects
from event_manager.event import Attribute, Event

OPERATION_RUN_CREATED = '{}.{}'.format(event_subjects.OPERATION_RUN,
                                       event_actions.CREATED)
OPERATION_RUN_UPDATED = '{}.{}'.format(event_subjects.OPERATION_RUN,
                                       event_actions.UPDATED)
OPERATION_RUN_DELETED = '{}.{}'.format(event_subjects.OPERATION_RUN,
                                       event_actions.DELETED)
OPERATION_RUN_VIEWED = '{}.{}'.format(event_subjects.OPERATION_RUN,
                                      event_actions.VIEWED)
OPERATION_RUN_ARCHIVED = '{}.{}'.format(event_subjects.OPERATION_RUN,
                                        event_actions.ARCHIVED)
OPERATION_RUN_RESTORED = '{}.{}'.format(event_subjects.OPERATION_RUN,
                                        event_actions.RESTORED)
OPERATION_RUN_STOPPED = '{}.{}'.format(event_subjects.OPERATION_RUN,
                                       event_actions.STOPPED)
OPERATION_RUN_RESUMED = '{}.{}'.format(event_subjects.OPERATION_RUN,
                                       event_actions.RESUMED)
OPERATION_RUN_RESTARTED = '{}.{}'.format(event_subjects.OPERATION_RUN,
                                         event_actions.RESTARTED)
OPERATION_RUN_SKIPPED = '{}.{}'.format(event_subjects.OPERATION_RUN,
                                       event_actions.SKIPPED)
OPERATION_RUN_NEW_STATUS = '{}.{}'.format(event_subjects.OPERATION_RUN,
                                          event_actions.NEW_STATUS)
OPERATION_RUN_SUCCEEDED = '{}.{}'.format(event_subjects.OPERATION_RUN,
                                         event_actions.SUCCEEDED)
OPERATION_RUN_FAILED = '{}.{}'.format(event_subjects.OPERATION_RUN,
                                      event_actions.FAILED)
OPERATION_RUN_DONE = '{}.{}'.format(event_subjects.OPERATION_RUN,
                                    event_actions.DONE)
OPERATION_RUN_DELETED_TRIGGERED = '{}.{}.{}'.format(event_subjects.OPERATION_RUN,
                                                    event_actions.DELETED,
                                                    event_subjects.TRIGGER)
OPERATION_RUN_CLEANED_TRIGGERED = '{}.{}.{}'.format(event_subjects.OPERATION_RUN,
                                                    event_actions.CLEANED,
                                                    event_subjects.TRIGGER)
OPERATION_RUN_STOPPED_TRIGGERED = '{}.{}.{}'.format(event_subjects.OPERATION_RUN,
                                                    event_actions.STOPPED,
                                                    event_subjects.TRIGGER)
OPERATION_RUN_RESUMED_TRIGGERED = '{}.{}.{}'.format(event_subjects.OPERATION_RUN,
                                                    event_actions.RESUMED,
                                                    event_subjects.TRIGGER)
OPERATION_RUN_RESTARTED_TRIGGERED = '{}.{}.{}'.format(event_subjects.OPERATION_RUN,
                                                      event_actions.RESTARTED,
                                                      event_subjects.TRIGGER)
OPERATION_RUN_SKIPPED_TRIGGERED = '{}.{}.{}'.format(event_subjects.OPERATION_RUN,
                                                    event_actions.SKIPPED,
                                                    event_subjects.TRIGGER)

EVENTS = {
    OPERATION_RUN_CREATED,
    OPERATION_RUN_UPDATED,
    OPERATION_RUN_DELETED,
    OPERATION_RUN_VIEWED,
    OPERATION_RUN_ARCHIVED,
    OPERATION_RUN_RESTORED,
    OPERATION_RUN_STOPPED,
    OPERATION_RUN_RESUMED,
    OPERATION_RUN_RESTARTED,
    OPERATION_RUN_SKIPPED,
    OPERATION_RUN_NEW_STATUS,
    OPERATION_RUN_SUCCEEDED,
    OPERATION_RUN_FAILED,
    OPERATION_RUN_DONE,
    OPERATION_RUN_DELETED_TRIGGERED,
    OPERATION_RUN_CLEANED_TRIGGERED,
    OPERATION_RUN_STOPPED_TRIGGERED,
    OPERATION_RUN_RESUMED_TRIGGERED,
    OPERATION_RUN_RESTARTED_TRIGGERED,
    OPERATION_RUN_SKIPPED_TRIGGERED
}


class OperationRunCreatedEvent(Event):
    event_type = OPERATION_RUN_CREATED
    actor = True
    attributes = (
        Attribute('id'),
        Attribute('operation.id'),
        Attribute('pipeline_run.id'),
        Attribute('created_at', is_datetime=True),
    )


class OperationRunUpdatedEvent(Event):
    event_type = OPERATION_RUN_UPDATED
    actor = True
    attributes = (
        Attribute('id'),
        Attribute('operation.id'),
        Attribute('pipeline_run.id'),
        Attribute('updated_at', is_datetime=True),
    )


class OperationRunDeletedEvent(Event):
    event_type = OPERATION_RUN_DELETED
    attributes = (
        Attribute('id'),
    )


class OperationRunViewedEvent(Event):
    event_type = OPERATION_RUN_VIEWED
    actor = True
    attributes = (
        Attribute('id'),
        Attribute('operation.id'),
        Attribute('pipeline_run.id'),
    )


class OperationRunArchivedEvent(Event):
    event_type = OPERATION_RUN_ARCHIVED
    actor = True
    attributes = (
        Attribute('id'),
        Attribute('operation.id'),
        Attribute('pipeline_run.id'),
    )


class OperationRunRestoredEvent(Event):
    event_type = OPERATION_RUN_RESTORED
    actor = True
    attributes = (
        Attribute('id'),
        Attribute('operation.id'),
        Attribute('pipeline_run.id'),
        Attribute('last_status'),
    )


class OperationRunStoppedEvent(Event):
    event_type = OPERATION_RUN_STOPPED
    attributes = (
        Attribute('id'),
        Attribute('operation.id'),
        Attribute('pipeline_run.id'),
        Attribute('last_status'),
        Attribute('previous_status', is_required=False),
    )


class OperationRunResumedEvent(Event):
    event_type = OPERATION_RUN_RESUMED
    attributes = (
        Attribute('id'),
        Attribute('operation.id'),
        Attribute('pipeline_run.id'),
        Attribute('last_status'),
        Attribute('previous_status', is_required=False),
    )


class OperationRunRestartedEvent(Event):
    event_type = OPERATION_RUN_RESTARTED
    attributes = (
        Attribute('id'),
        Attribute('operation.id'),
        Attribute('pipeline_run.id'),
        Attribute('last_status'),
    )


class OperationRunSkippedEvent(Event):
    event_type = OPERATION_RUN_SKIPPED
    attributes = (
        Attribute('id'),
        Attribute('operation.id'),
        Attribute('pipeline_run.id'),
        Attribute('last_status'),
    )


class OperationRunNewStatusEvent(Event):
    event_type = OPERATION_RUN_NEW_STATUS
    attributes = (
        Attribute('id'),
        Attribute('operation.id'),
        Attribute('pipeline_run.id'),
        Attribute('last_status'),
        Attribute('previous_status', is_required=False),
    )


class OperationRunSucceededEvent(Event):
    event_type = OPERATION_RUN_SUCCEEDED
    attributes = (
        Attribute('id'),
        Attribute('operation.id'),
        Attribute('pipeline_run.id'),
        Attribute('previous_status', is_required=False),
    )


class OperationRunFailedEvent(Event):
    event_type = OPERATION_RUN_FAILED
    attributes = (
        Attribute('id'),
        Attribute('operation.id'),
        Attribute('pipeline_run.id'),
        Attribute('last_status'),
        Attribute('previous_status', is_required=False),
    )


class OperationRunDoneEvent(Event):
    event_type = OPERATION_RUN_DONE
    attributes = (
        Attribute('id'),
        Attribute('operation.id'),
        Attribute('pipeline_run.id'),
        Attribute('last_status'),
        Attribute('previous_status', is_required=False),
    )


class OperationRunDeletedTriggeredEvent(Event):
    event_type = OPERATION_RUN_DELETED_TRIGGERED
    actor = True
    attributes = (
        Attribute('id'),
        Attribute('operation.id'),
        Attribute('pipeline_run.id'),
        Attribute('last_status'),
    )


class OperationRunCleanedTriggeredEvent(Event):
    event_type = OPERATION_RUN_CLEANED_TRIGGERED
    attributes = (
        Attribute('id'),
    )


class OperationRunStoppedTriggeredEvent(Event):
    event_type = OPERATION_RUN_STOPPED_TRIGGERED
    actor = True
    attributes = (
        Attribute('id'),
        Attribute('operation.id'),
        Attribute('pipeline_run.id'),
        Attribute('last_status'),
    )


class OperationRunResumedTriggeredEvent(Event):
    event_type = OPERATION_RUN_RESUMED_TRIGGERED
    actor = True
    attributes = (
        Attribute('id'),
        Attribute('operation.id'),
        Attribute('pipeline_run.id'),
        Attribute('last_status'),
    )


class OperationRunRestartedTriggeredEvent(Event):
    event_type = OPERATION_RUN_RESTARTED_TRIGGERED
    actor = True
    attributes = (
        Attribute('id'),
        Attribute('operation.id'),
        Attribute('pipeline_run.id'),
        Attribute('last_status'),
    )


class OperationRunSkippedTriggeredEvent(Event):
    event_type = OPERATION_RUN_SKIPPED_TRIGGERED
    actor = True
    attributes = (
        Attribute('id'),
        Attribute('operation.id'),
        Attribute('pipeline_run.id'),
        Attribute('last_status'),
    )
