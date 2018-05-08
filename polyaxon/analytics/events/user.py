import analytics
from event_manager.events import user

analytics.register(user.UserRegisteredEvent)
analytics.register(user.UserUpdatedEvent)
analytics.register(user.UserActivatedEvent)
analytics.register(user.UserDeletedEvent)
