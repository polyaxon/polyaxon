import auditor
from libs.event_manager import event_types
from libs.event_manager.event import Event


class UserRegisteredEvent(Event):
    type = event_types.USER_REGISTERED


class UserPasswordUpdatedEvent(Event):
    type = event_types.USER_PASSWORD_UPDATED


class UserActivatedEvent(Event):
    type = event_types.USER_ACTIVATED


class UserDeletedEvent(Event):
    type = event_types.USER_DELETED


auditor.register(UserRegisteredEvent)
auditor.register(UserPasswordUpdatedEvent)
auditor.register(UserActivatedEvent)
auditor.register(UserDeletedEvent)
