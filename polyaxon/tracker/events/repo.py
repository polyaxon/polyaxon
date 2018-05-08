import tracker

from event_manager.events import repo

tracker.subscribe(repo.RepoCreatedEvent)
tracker.subscribe(repo.RepoNewCommitEvent)
