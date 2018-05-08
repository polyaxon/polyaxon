import analytics
from event_manager.events import repo

analytics.subscribe(repo.RepoCreatedEvent)
analytics.subscribe(repo.RepoNewCommitEvent)
