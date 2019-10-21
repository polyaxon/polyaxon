import activitylogs

from events.registry import repo

activitylogs.subscribe(repo.RepoCreatedEvent)
activitylogs.subscribe(repo.RepoDownloadedEvent)
activitylogs.subscribe(repo.RepoNewCommitEvent)
