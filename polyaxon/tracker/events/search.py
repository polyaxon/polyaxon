import tracker

from event_manager.events import search

tracker.subscribe(search.SearchCreatedEvent)
tracker.subscribe(search.SearchDeletedEvent)
