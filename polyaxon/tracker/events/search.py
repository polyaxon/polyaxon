import tracker

from events.registry import search

tracker.subscribe(search.SearchCreatedEvent)
tracker.subscribe(search.SearchDeletedEvent)
