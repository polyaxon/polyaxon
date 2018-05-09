from event_manager import event_actions, event_subjects
from event_manager.event import Attribute, Event

USER_REGISTERED = '{}.{}'.format(event_subjects.USER, event_actions.REGISTERED)
USER_UPDATED = '{}.{}'.format(event_subjects.USER, event_actions.UPDATED)
USER_ACTIVATED = '{}.{}'.format(event_subjects.USER, event_actions.ACTIVATED)
USER_DELETED = '{}.{}'.format(event_subjects.USER, event_actions.DELETED)


class UserRegisteredEvent(Event):
    event_type = USER_REGISTERED
    actor_id = 'id'
    attributes = (
        Attribute('id', is_uuid=True),
        Attribute('created_at', is_datetime=True)
    )


class UserUpdatedEvent(Event):
    event_type = USER_UPDATED
    actor_id = 'id'
    attributes = (
        Attribute('id'),
        Attribute('updated_at', is_datetime=True)
    )


class UserActivatedEvent(Event):
    event_type = USER_ACTIVATED
    actor_id = 'actor_id'
    attributes = (
        Attribute('id'),
        Attribute('actor_id')
    )


class UserDeletedEvent(Event):
    event_type = USER_DELETED
    actor_id = 'actor_id'
    attributes = (
        Attribute('id'),
        Attribute('actor_id')
    )
