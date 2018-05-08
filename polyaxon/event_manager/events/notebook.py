from event_manager.event import Event, Attribute

NOTEBOOK_STARTED = 'notebook.started'
NOTEBOOK_STOPPED = 'notebook.stopped'
NOTEBOOK_VIEWED = 'notebook.stopped'
NOTEBOOK_NEW_STATUS = 'notebook.new_status'


class NotebookStartedEvent(Event):
    type = NOTEBOOK_STARTED
    attributes = (
        Attribute('notebook_uuid', is_uuid=True),
        Attribute('project_uuid', is_uuid=True),
        Attribute('project_owner_uuid', is_uuid=True),
        Attribute('actor_uuid', is_uuid=True)
    )


class NotebookSoppedEvent(Event):
    type = NOTEBOOK_STOPPED
    attributes = (
        Attribute('notebook_uuid', is_uuid=True),
        Attribute('project_uuid', is_uuid=True),
        Attribute('project_owner_uuid', is_uuid=True),
        Attribute('actor_uuid', is_uuid=True)
    )


class NotebookViewedEvent(Event):
    type = NOTEBOOK_VIEWED
    attributes = (
        Attribute('notebook_uuid', is_uuid=True),
        Attribute('project_uuid', is_uuid=True),
        Attribute('project_owner_uuid', is_uuid=True),
        Attribute('actor_uuid', is_uuid=True)
    )


class NotebookNewStatusEvent(Event):
    type = NOTEBOOK_NEW_STATUS
    attributes = (
        Attribute('notebook_uuid', is_uuid=True),
        Attribute('project_uuid', is_uuid=True),
        Attribute('statue')
    )
