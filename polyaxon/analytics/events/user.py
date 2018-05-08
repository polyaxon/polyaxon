import analytics
from event_manager.events import user

analytics.subscribe(user.UserRegisteredEvent)
analytics.subscribe(user.UserUpdatedEvent)
analytics.subscribe(user.UserActivatedEvent)
analytics.subscribe(user.UserDeletedEvent)
