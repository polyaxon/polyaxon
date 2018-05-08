import auditor
from event_manager.events import repo

auditor.subscribe(repo.RepoCreatedEvent)
auditor.subscribe(repo.RepoNewCommitEvent)
