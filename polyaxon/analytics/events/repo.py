import analytics
from libs.event_manager.base_events import repo

analytics.register(repo.RepoCreatedEvent)
analytics.register(repo.RepoNewCommitEvent)
