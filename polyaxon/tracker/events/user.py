import tracker

from event_manager.events import user

tracker.subscribe(user.UserRegisteredEvent)
tracker.subscribe(user.UserUpdatedEvent)
tracker.subscribe(user.UserActivatedEvent)
tracker.subscribe(user.UserDeletedEvent)
