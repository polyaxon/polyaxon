from event_manager.event import Event, Attribute

REPO_CREATED = 'repo.created'
REPO_NEW_COMMIT = 'repo.new_commit'


class RepoCreatedEvent(Event):
    type = REPO_CREATED
    attributes = (
        Attribute('repo_uuid', is_uuid=True),
        Attribute('project_uuid', is_uuid=True),
        Attribute('project_owner_uuid', is_uuid=True),
        Attribute('actor_uuid', is_uuid=True),
    )


class RepoNewCommitEvent(Event):
    type = REPO_NEW_COMMIT
    attributes = (
        Attribute('repo_uuid', is_uuid=True),
        Attribute('project_uuid', is_uuid=True),
        Attribute('project_owner_uuid', is_uuid=True),
        Attribute('actor_uuid', is_uuid=True),
    )
