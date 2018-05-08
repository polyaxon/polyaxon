import analytics
from event_manager.events import repo

analytics.register(repo.RepoCreatedEvent)
analytics.register(repo.RepoNewCommitEvent)
