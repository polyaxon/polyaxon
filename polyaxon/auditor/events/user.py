import auditor
from libs.event_manager.base_events import user

auditor.register(user.UserRegisteredEvent)
auditor.register(user.UserUpdatedEvent)
auditor.register(user.UserActivatedEvent)
auditor.register(user.UserDeletedEvent)
