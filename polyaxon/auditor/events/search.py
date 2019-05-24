import auditor

from events.registry import search

auditor.subscribe(search.SearchCreatedEvent)
auditor.subscribe(search.SearchDeletedEvent)
