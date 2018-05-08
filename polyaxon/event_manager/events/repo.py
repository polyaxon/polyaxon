from event_manager.event import Event, Attribute

REPO_CREATED = 'repo.created'
REPO_NEW_COMMIT = 'repo.new_commit'


class RepoCreatedEvent(Event):
    type = REPO_CREATED
    attributes = (
        Attribute('id'),
        Attribute('project.id'),
        Attribute('project.user.id'),
        Attribute('actor_id'),
    )


class RepoNewCommitEvent(Event):
    type = REPO_NEW_COMMIT
    attributes = (
        Attribute('id'),
        Attribute('project.id'),
        Attribute('project.user.id'),
        Attribute('actor_id'),
    )
