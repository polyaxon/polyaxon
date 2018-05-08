import auditor
from event_manager.events import user

auditor.register(user.UserRegisteredEvent)
auditor.register(user.UserUpdatedEvent)
auditor.register(user.UserActivatedEvent)
auditor.register(user.UserDeletedEvent)
