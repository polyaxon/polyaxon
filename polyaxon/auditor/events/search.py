import auditor

from event_manager.events import search

auditor.subscribe(search.SearchCreatedEvent)
