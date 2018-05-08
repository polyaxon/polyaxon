from libs.event_manager.event import Event

REPO_CREATED = 'repo.created'
REPO_NEW_COMMIT = 'repo.new_commit'  # attempt, fullfilled


class RepoCreatedEvent(Event):
    type = REPO_CREATED


class RepoNewCommitEvent(Event):
    type = REPO_NEW_COMMIT
