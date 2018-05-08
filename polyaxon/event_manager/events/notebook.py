from event_manager.event import Event, Attribute

NOTEBOOK_STARTED = 'notebook.started'
NOTEBOOK_STOPPED = 'notebook.stopped'
NOTEBOOK_VIEWED = 'notebook.stopped'
NOTEBOOK_NEW_STATUS = 'notebook.new_status'


class NotebookStartedEvent(Event):
    type = NOTEBOOK_STARTED
    attributes = (
        Attribute('id'),
        Attribute('project.id'),
        Attribute('project.user.id'),
        Attribute('actor_id')
    )


class NotebookSoppedEvent(Event):
    type = NOTEBOOK_STOPPED
    attributes = (
        Attribute('id'),
        Attribute('project.id'),
        Attribute('project.user.id'),
        Attribute('actor_id'),
        Attribute('status'),
    )


class NotebookViewedEvent(Event):
    type = NOTEBOOK_VIEWED
    attributes = (
        Attribute('id'),
        Attribute('project.id'),
        Attribute('project.user.id'),
        Attribute('actor_id'),
        Attribute('status'),
    )


class NotebookNewStatusEvent(Event):
    type = NOTEBOOK_NEW_STATUS
    attributes = (
        Attribute('id'),
        Attribute('project.id'),
        Attribute('status')
    )
