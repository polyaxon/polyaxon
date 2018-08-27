import activitylogs

from event_manager.events import search

activitylogs.subscribe(search.SearchCreatedEvent)
