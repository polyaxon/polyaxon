from event_manager import event_actions, event_subjects
from event_manager.event import Attribute, Event

PIPELINE_CREATED = '{}.{}'.format(event_subjects.PIPELINE,
                                  event_actions.CREATED)
PIPELINE_UPDATED = '{}.{}'.format(event_subjects.PIPELINE,
                                  event_actions.UPDATED)
PIPELINE_DELETED = '{}.{}'.format(event_subjects.PIPELINE,
                                  event_actions.DELETED)
PIPELINE_VIEWED = '{}.{}'.format(event_subjects.PIPELINE,
                                 event_actions.VIEWED)
PIPELINE_ARCHIVED = '{}.{}'.format(event_subjects.PIPELINE,
                                   event_actions.ARCHIVED)
PIPELINE_RESTORED = '{}.{}'.format(event_subjects.PIPELINE,
                                   event_actions.RESTORED)
PIPELINE_BOOKMARKED = '{}.{}'.format(event_subjects.PIPELINE,
                                     event_actions.BOOKMARKED)
PIPELINE_UNBOOKMARKED = '{}.{}'.format(event_subjects.PIPELINE,
                                       event_actions.UNBOOKMARKED)
PIPELINE_DELETED_TRIGGERED = '{}.{}.{}'.format(event_subjects.PIPELINE,
                                               event_actions.DELETED,
                                               event_subjects.TRIGGER)
PIPELINE_CLEANED_TRIGGERED = '{}.{}.{}'.format(event_subjects.PIPELINE,
                                               event_actions.CLEANED,
                                               event_subjects.TRIGGER)

EVENTS = {
    PIPELINE_CREATED,
    PIPELINE_UPDATED,
    PIPELINE_DELETED,
    PIPELINE_VIEWED,
    PIPELINE_ARCHIVED,
    PIPELINE_RESTORED,
    PIPELINE_BOOKMARKED,
    PIPELINE_UNBOOKMARKED,
    PIPELINE_DELETED_TRIGGERED,
    PIPELINE_CLEANED_TRIGGERED,
}


class PipelineCreatedEvent(Event):
    event_type = PIPELINE_CREATED
    actor = True
    actor_id = 'user.id'
    actor_name = 'user.username'
    attributes = (
        Attribute('id'),
        Attribute('project.id'),
        Attribute('project.user.id'),
        Attribute('created_at', is_datetime=True),
        Attribute('has_description', attr_type=bool),
        Attribute('backend', attr_type=bool),
        Attribute('is_managed', attr_type=bool),
        Attribute('has_specification', attr_type=bool),
    )


class PipelineUpdatedEvent(Event):
    event_type = PIPELINE_UPDATED
    actor = True
    attributes = (
        Attribute('id'),
        Attribute('user.id'),
        Attribute('project.id'),
        Attribute('project.user.id'),
        Attribute('backend', attr_type=bool),
        Attribute('is_managed', attr_type=bool),
        Attribute('updated_at', is_datetime=True),
        Attribute('has_description', attr_type=bool),
    )


class PipelineDeletedEvent(Event):
    event_type = PIPELINE_DELETED
    attributes = (
        Attribute('id'),
    )


class PipelineViewedEvent(Event):
    event_type = PIPELINE_VIEWED
    actor = True
    attributes = (
        Attribute('id'),
        Attribute('user.id'),
        Attribute('project.id'),
        Attribute('project.user.id'),
        Attribute('backend', attr_type=bool),
        Attribute('is_managed', attr_type=bool),
        Attribute('has_description', attr_type=bool),
    )


class PipelineArchivedEvent(Event):
    event_type = PIPELINE_ARCHIVED
    actor = True
    attributes = (
        Attribute('id'),
        Attribute('project.id'),
        Attribute('project.user.id'),
        Attribute('backend', attr_type=bool),
        Attribute('is_managed', attr_type=bool),
        Attribute('user.id'),
    )


class PipelineRestoredEvent(Event):
    event_type = PIPELINE_RESTORED
    actor = True
    attributes = (
        Attribute('id'),
        Attribute('user.id'),
        Attribute('project.id'),
        Attribute('project.user.id'),
        Attribute('backend', attr_type=bool),
        Attribute('is_managed', attr_type=bool),
    )


class PipelineBookmarkedEvent(Event):
    event_type = PIPELINE_BOOKMARKED
    actor = True
    attributes = (
        Attribute('id'),
        Attribute('user.id'),
        Attribute('project.id'),
        Attribute('project.user.id'),
        Attribute('backend', attr_type=bool),
        Attribute('is_managed', attr_type=bool),
    )


class PipelineUnbookmarkedEvent(Event):
    event_type = PIPELINE_UNBOOKMARKED
    actor = True
    attributes = (
        Attribute('id'),
        Attribute('user.id'),
        Attribute('project.id'),
        Attribute('project.user.id'),
        Attribute('backend', attr_type=bool),
        Attribute('is_managed', attr_type=bool),
    )


class PipelineDeletedTriggeredEvent(Event):
    event_type = PIPELINE_DELETED_TRIGGERED
    actor = True
    attributes = (
        Attribute('id'),
        Attribute('user.id'),
        Attribute('project.id'),
        Attribute('project.user.id'),
        Attribute('backend', attr_type=bool),
        Attribute('is_managed', attr_type=bool),
        Attribute('updated_at', is_datetime=True),
        Attribute('has_description', attr_type=bool),
    )


class PipelineCleanedTriggeredEvent(Event):
    event_type = PIPELINE_CLEANED_TRIGGERED
    attributes = (
        Attribute('id'),
    )
