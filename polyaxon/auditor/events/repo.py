import auditor
from event_manager.events import repo

auditor.register(repo.RepoCreatedEvent)
auditor.register(repo.RepoNewCommitEvent)
