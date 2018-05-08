import auditor
from libs.event_manager.base_events import repo

auditor.register(repo.RepoCreatedEvent)
auditor.register(repo.RepoNewCommitEvent)
