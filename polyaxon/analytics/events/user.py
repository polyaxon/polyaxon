import analytics
from libs.event_manager.base_events import user

analytics.register(user.UserRegisteredEvent)
analytics.register(user.UserUpdatedEvent)
analytics.register(user.UserActivatedEvent)
analytics.register(user.UserDeletedEvent)
