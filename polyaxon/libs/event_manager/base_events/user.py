from libs.event_manager.event import Attribute, Event

USER_REGISTERED = 'user.registered'
USER_UPDATED = 'user.updated'
USER_ACTIVATED = 'user.activated'
USER_DELETED = 'user.deleted'


class UserRegisteredEvent(Event):
    type = USER_REGISTERED

    attributes = (
        Attribute('created_at', is_datetime=True)
    )


class UserUpdatedEvent(Event):
    type = USER_UPDATED

    attributes = (
        Attribute('updated_at', is_datetime=True)
    )


class UserActivatedEvent(Event):
    type = USER_ACTIVATED


class UserDeletedEvent(Event):
    type = USER_DELETED
