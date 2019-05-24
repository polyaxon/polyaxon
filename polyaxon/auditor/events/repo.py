import auditor

from events.registry import repo

auditor.subscribe(repo.RepoCreatedEvent)
auditor.subscribe(repo.RepoDownloadedEvent)
auditor.subscribe(repo.RepoNewCommitEvent)
