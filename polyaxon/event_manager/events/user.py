from event_manager.event import Attribute, Event

USER_REGISTERED = 'user.registered'
USER_UPDATED = 'user.updated'
USER_ACTIVATED = 'user.activated'
USER_DELETED = 'user.deleted'


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
        Attribute('id', is_uuid=True),
        Attribute('updated_at', is_datetime=True)
    )


class UserActivatedEvent(Event):
    event_type = USER_ACTIVATED
    actor_id = 'actor_id'
    attributes = (
        Attribute('id', is_uuid=True),
        Attribute('actor_id', is_uuid=True)
    )


class UserDeletedEvent(Event):
    event_type = USER_DELETED
    actor_id = 'actor_id'
    attributes = (
        Attribute('id', is_uuid=True),
        Attribute('actor_id', is_uuid=True)
    )
