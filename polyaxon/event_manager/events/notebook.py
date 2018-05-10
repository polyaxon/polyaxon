from event_manager import event_actions, event_subjects
from event_manager.event import Attribute, Event

NOTEBOOK_STARTED = '{}.{}'.format(event_subjects.NOTEBOOK, event_actions.STARTED)
NOTEBOOK_STOPPED = '{}.{}'.format(event_subjects.NOTEBOOK, event_actions.STOPPED)
NOTEBOOK_VIEWED = '{}.{}'.format(event_subjects.NOTEBOOK, event_actions.VIEWED)
NOTEBOOK_NEW_STATUS = '{}.{}'.format(event_subjects.NOTEBOOK, event_actions.NEW_STATUS)


class NotebookStartedEvent(Event):
    event_type = NOTEBOOK_STARTED
    actor_id = 'actor_id'
    attributes = (
        Attribute('id'),
        Attribute('project.id'),
        Attribute('project.user.id'),
        Attribute('actor_id')
    )


class NotebookSoppedEvent(Event):
    event_type = NOTEBOOK_STOPPED
    actor_id = 'actor_id'
    attributes = (
        Attribute('id'),
        Attribute('project.id'),
        Attribute('project.user.id'),
        Attribute('actor_id'),
        Attribute('last_status'),
    )


class NotebookViewedEvent(Event):
    event_type = NOTEBOOK_VIEWED
    actor_id = 'actor_id'
    attributes = (
        Attribute('id'),
        Attribute('project.id'),
        Attribute('project.user.id'),
        Attribute('actor_id'),
        Attribute('last_status'),
    )


class NotebookNewStatusEvent(Event):
    event_type = NOTEBOOK_NEW_STATUS
    attributes = (
        Attribute('id'),
        Attribute('project.id'),
        Attribute('last_status')
    )
