import activitylogs

from event_manager.events import user

activitylogs.subscribe(user.UserRegisteredEvent)
activitylogs.subscribe(user.UserUpdatedEvent)
activitylogs.subscribe(user.UserActivatedEvent)
activitylogs.subscribe(user.UserDeletedEvent)
