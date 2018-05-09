from event_manager import event_subjects, event_actions
from event_manager.event import Attribute, Event

REPO_CREATED = '{}.{}'.format(event_subjects.REPO, event_actions.CREATED)
REPO_NEW_COMMIT = '{}.new_commit'.format(event_subjects.REPO)


class RepoCreatedEvent(Event):
    event_type = REPO_CREATED
    actor_id = 'actor_id'
    attributes = (
        Attribute('id'),
        Attribute('project.id'),
        Attribute('project.user.id'),
        Attribute('actor_id'),
    )


class RepoNewCommitEvent(Event):
    event_type = REPO_NEW_COMMIT
    actor_id = 'actor_id'
    attributes = (
        Attribute('id'),
        Attribute('project.id'),
        Attribute('project.user.id'),
        Attribute('actor_id'),
    )
