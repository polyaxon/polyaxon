from event_manager import event_actions, event_subjects
from event_manager.event import Attribute, Event

NOTEBOOK_STARTED = '{}.{}'.format(event_subjects.NOTEBOOK, event_actions.STARTED)
NOTEBOOK_STARTED_TRIGGERED = '{}.{}.{}'.format(event_subjects.NOTEBOOK,
                                               event_actions.STARTED,
                                               event_subjects.TRIGGER)
NOTEBOOK_STOPPED = '{}.{}'.format(event_subjects.NOTEBOOK, event_actions.STOPPED)
NOTEBOOK_STOPPED_TRIGGERED = '{}.{}.{}'.format(event_subjects.NOTEBOOK,
                                               event_actions.STOPPED,
                                               event_subjects.TRIGGER)
NOTEBOOK_VIEWED = '{}.{}'.format(event_subjects.NOTEBOOK, event_actions.VIEWED)
NOTEBOOK_NEW_STATUS = '{}.{}'.format(event_subjects.NOTEBOOK, event_actions.NEW_STATUS)
NOTEBOOK_FAILED = '{}.{}'.format(event_subjects.NOTEBOOK, event_actions.FAILED)
NOTEBOOK_SUCCEEDED = '{}.{}'.format(event_subjects.NOTEBOOK, event_actions.SUCCEEDED)


class NotebookStartedEvent(Event):
    event_type = NOTEBOOK_STARTED
    attributes = (
        Attribute('id'),
        Attribute('user.id'),
        Attribute('project.id'),
        Attribute('project.user.id'),
        Attribute('target'),  # project, experiment_group, experiment
    )


class NotebookStartedTriggeredEvent(Event):
    event_type = NOTEBOOK_STARTED_TRIGGERED
    actor_id = 'actor_id'
    attributes = (
        Attribute('id'),
        Attribute('user.id'),
        Attribute('project.id'),
        Attribute('project.user.id'),
        Attribute('target'),  # project, experiment_group, experiment
        Attribute('actor_id'),
    )


class NotebookSoppedEvent(Event):
    event_type = NOTEBOOK_STOPPED
    attributes = (
        Attribute('id'),
        Attribute('user.id'),
        Attribute('project.id'),
        Attribute('project.user.id'),
        Attribute('target'),  # project, experiment_group, experiment
        Attribute('last_status'),
        Attribute('previous_status', is_required=False),
    )


class NotebookSoppedTriggeredEvent(Event):
    event_type = NOTEBOOK_STOPPED_TRIGGERED
    actor_id = 'actor_id'
    attributes = (
        Attribute('id'),
        Attribute('user.id'),
        Attribute('project.id'),
        Attribute('project.user.id'),
        Attribute('target'),  # project, experiment_group, experiment
        Attribute('actor_id'),
        Attribute('last_status'),
    )


class NotebookViewedEvent(Event):
    event_type = NOTEBOOK_VIEWED
    actor_id = 'actor_id'
    attributes = (
        Attribute('id'),
        Attribute('user.id'),
        Attribute('project.id'),
        Attribute('project.user.id'),
        Attribute('actor_id'),
        Attribute('last_status'),
        Attribute('target'),  # project, experiment_group, experiment
    )


class NotebookNewStatusEvent(Event):
    event_type = NOTEBOOK_NEW_STATUS
    attributes = (
        Attribute('id'),
        Attribute('user.id'),
        Attribute('project.id'),
        Attribute('last_status'),
        Attribute('target'),  # project, experiment_group, experiment
    )


class NotebookSucceededEvent(Event):
    event_type = NOTEBOOK_SUCCEEDED
    attributes = (
        Attribute('id'),
        Attribute('user.id'),
        Attribute('project.id'),
        Attribute('last_status'),
        Attribute('previous_status', is_required=False),
        Attribute('target'),  # project, experiment_group, experiment
    )


class NotebookFailedEvent(Event):
    event_type = NOTEBOOK_FAILED
    attributes = (
        Attribute('id'),
        Attribute('user.id'),
        Attribute('project.id'),
        Attribute('last_status'),
        Attribute('previous_status', is_required=False),
        Attribute('target'),  # project, experiment_group, experiment
    )
