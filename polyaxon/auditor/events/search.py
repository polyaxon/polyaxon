import auditor

from event_manager.events import search

auditor.subscribe(search.SearchCreatedEvent)
auditor.subscribe(search.SearchDeletedEvent)
