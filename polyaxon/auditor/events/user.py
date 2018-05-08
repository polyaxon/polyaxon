import auditor

from event_manager.events import user

auditor.subscribe(user.UserRegisteredEvent)
auditor.subscribe(user.UserUpdatedEvent)
auditor.subscribe(user.UserActivatedEvent)
auditor.subscribe(user.UserDeletedEvent)
