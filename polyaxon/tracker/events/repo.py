import tracker

from events.registry import repo

tracker.subscribe(repo.RepoCreatedEvent)
tracker.subscribe(repo.RepoDownloadedEvent)
tracker.subscribe(repo.RepoNewCommitEvent)
