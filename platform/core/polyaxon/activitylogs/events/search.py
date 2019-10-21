import activitylogs

from events.registry import search

activitylogs.subscribe(search.SearchCreatedEvent)
activitylogs.subscribe(search.SearchDeletedEvent)
