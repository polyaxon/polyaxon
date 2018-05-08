from libs.event_manager.event import Event

USER_REGISTERED = 'user.registered'
USER_UPDATED = 'user.updated'
USER_ACTIVATED = 'user.activated'
USER_DELETED = 'user.deleted'


class UserRegisteredEvent(Event):
    type = USER_REGISTERED


class UserUpdatedEvent(Event):
    type = USER_UPDATED


class UserActivatedEvent(Event):
    type = USER_ACTIVATED


class UserDeletedEvent(Event):
    type = USER_DELETED
