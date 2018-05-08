import activitylogs

from event_manager.events import repo

activitylogs.subscribe(repo.RepoCreatedEvent)
activitylogs.subscribe(repo.RepoNewCommitEvent)
