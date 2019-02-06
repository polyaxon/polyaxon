from event_manager import event_actions, event_subjects
from event_manager.event import Attribute, Event

REPO_CREATED = '{}.{}'.format(event_subjects.REPO, event_actions.CREATED)
REPO_DOWNLOADED = '{}.{}'.format(event_subjects.REPO, event_actions.DOWNLOADED)
REPO_NEW_COMMIT = '{}.new_commit'.format(event_subjects.REPO)


class RepoCreatedEvent(Event):
    event_type = REPO_CREATED
    actor = True
    attributes = (
        Attribute('id'),
        Attribute('project.id'),
        Attribute('project.user.id'),
        Attribute('external', attr_type=bool)
    )


class RepoDownloadedEvent(Event):
    event_type = REPO_DOWNLOADED
    actor = True
    attributes = (
        Attribute('id'),
        Attribute('project.id'),
        Attribute('project.user.id'),
    )


class RepoNewCommitEvent(Event):
    event_type = REPO_NEW_COMMIT
    actor = True
    attributes = (
        Attribute('id'),
        Attribute('project.id'),
        Attribute('project.user.id'),
    )
