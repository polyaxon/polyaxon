from event_manager.event import Attribute, Event

REPO_CREATED = 'repo.created'
REPO_NEW_COMMIT = 'repo.new_commit'


class RepoCreatedEvent(Event):
    event_type = REPO_CREATED
    attributes = (
        Attribute('id'),
        Attribute('project.id'),
        Attribute('project.user.id'),
        Attribute('actor_id'),
    )


class RepoNewCommitEvent(Event):
    event_type = REPO_NEW_COMMIT
    attributes = (
        Attribute('id'),
        Attribute('project.id'),
        Attribute('project.user.id'),
        Attribute('actor_id'),
    )
