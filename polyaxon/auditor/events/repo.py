import auditor
from libs.event_manager import event_types
from libs.event_manager.event import Event


class RepoCreatedEvent(Event):
    type = event_types.REPO_CREATED


class RepoNewCommitEvent(Event):
    type = event_types.REPO_NEW_COMMIT


auditor.register(RepoCreatedEvent)
auditor.register(RepoNewCommit)
