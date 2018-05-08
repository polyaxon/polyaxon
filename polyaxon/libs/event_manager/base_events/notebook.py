from libs.event_manager.event import Event

NOTEBOOK_STARTED = 'notebook.started'
NOTEBOOK_STOPPED = 'notebook.stopped'
NOTEBOOK_NEW_STATUS = 'notebook.new_status'


class NotebookStartedEvent(Event):
    type = NOTEBOOK_STARTED


class NotebookSoppedEvent(Event):
    type = NOTEBOOK_STOPPED


class NotebookNewStatusEvent(Event):
    type = NOTEBOOK_NEW_STATUS
