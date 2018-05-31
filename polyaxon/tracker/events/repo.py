import tracker

from event_manager.events import repo

tracker.subscribe(repo.RepoCreatedEvent)
tracker.subscribe(repo.RepoDownloadedEvent)
tracker.subscribe(repo.RepoNewCommitEvent)
