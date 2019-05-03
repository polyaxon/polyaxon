from event_manager import event_actions, event_subjects
from event_manager.event import Attribute, Event

OPERATION_CREATED = '{}.{}'.format(event_subjects.OPERATION,
                                   event_actions.CREATED)
OPERATION_UPDATED = '{}.{}'.format(event_subjects.OPERATION,
                                   event_actions.UPDATED)
OPERATION_DELETED = '{}.{}'.format(event_subjects.OPERATION,
                                   event_actions.DELETED)
OPERATION_VIEWED = '{}.{}'.format(event_subjects.OPERATION,
                                  event_actions.VIEWED)
OPERATION_ARCHIVED = '{}.{}'.format(event_subjects.OPERATION,
                                    event_actions.ARCHIVED)
OPERATION_RESTORED = '{}.{}'.format(event_subjects.OPERATION,
                                    event_actions.RESTORED)
OPERATION_DELETED_TRIGGERED = '{}.{}.{}'.format(event_subjects.EXPERIMENT,
                                                 event_actions.DELETED,
                                                 event_subjects.TRIGGER)
OPERATION_CLEANED_TRIGGERED = '{}.{}.{}'.format(event_subjects.EXPERIMENT,
                                                 event_actions.CLEANED,
                                                 event_subjects.TRIGGER)


class OperationCreatedEvent(Event):
    event_type = OPERATION_CREATED
    actor = True
    actor_id = 'user.id'
    actor_name = 'user.username'
    attributes = (
        Attribute('id'),
        Attribute('project.id'),
        Attribute('project.user.id'),
        Attribute('pipeline.id'),
        Attribute('pipeline.user.id'),
        Attribute('created_at', is_datetime=True),
        Attribute('has_description', attr_type=bool),
        Attribute('backend', attr_type=bool),
        Attribute('is_managed', attr_type=bool),
        Attribute('has_specification', attr_type=bool),
    )


class OperationUpdatedEvent(Event):
    event_type = OPERATION_UPDATED
    actor = True
    attributes = (
        Attribute('id'),
        Attribute('user.id'),
        Attribute('project.id'),
        Attribute('project.user.id'),
        Attribute('pipeline.id'),
        Attribute('pipeline.user.id'),
        Attribute('backend', attr_type=bool),
        Attribute('is_managed', attr_type=bool),
        Attribute('updated_at', is_datetime=True),
        Attribute('has_description', attr_type=bool),
    )


class OperationDeletedEvent(Event):
    event_type = OPERATION_DELETED
    attributes = (
        Attribute('id'),
    )


class OperationViewedEvent(Event):
    event_type = OPERATION_VIEWED
    actor = True
    attributes = (
        Attribute('id'),
        Attribute('user.id'),
        Attribute('project.id'),
        Attribute('project.user.id'),
        Attribute('pipeline.id'),
        Attribute('pipeline.user.id'),
        Attribute('backend', attr_type=bool),
        Attribute('is_managed', attr_type=bool),
        Attribute('has_description', attr_type=bool),
    )


class OperationArchivedEvent(Event):
    event_type = OPERATION_ARCHIVED
    actor = True
    attributes = (
        Attribute('id'),
        Attribute('project.id'),
        Attribute('project.user.id'),
        Attribute('pipeline.id'),
        Attribute('pipeline.user.id'),
        Attribute('backend', attr_type=bool),
        Attribute('is_managed', attr_type=bool),
        Attribute('user.id'),
    )


class OperationRestoredEvent(Event):
    event_type = OPERATION_RESTORED
    actor = True
    attributes = (
        Attribute('id'),
        Attribute('user.id'),
        Attribute('project.id'),
        Attribute('project.user.id'),
        Attribute('pipeline.id'),
        Attribute('pipeline.user.id'),
        Attribute('backend', attr_type=bool),
        Attribute('is_managed', attr_type=bool),
    )


class OperationDeletedTriggeredEvent(Event):
    event_type = OPERATION_DELETED_TRIGGERED
    actor = True
    attributes = (
        Attribute('id'),
        Attribute('user.id'),
        Attribute('project.id'),
        Attribute('project.user.id'),
        Attribute('pipeline.id'),
        Attribute('pipeline.user.id'),
        Attribute('backend', attr_type=bool),
        Attribute('is_managed', attr_type=bool),
        Attribute('updated_at', is_datetime=True),
        Attribute('has_description', attr_type=bool),
    )


class OperationCleanedTriggeredEvent(Event):
    event_type = OPERATION_CLEANED_TRIGGERED
    attributes = (
        Attribute('id'),
    )
