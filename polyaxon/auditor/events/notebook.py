import auditor
from libs.event_manager import event_types
from libs.event_manager.event import Event


class NotebookStartedEvent(Event):
    type = event_types.NOTEBOOK_STARTED


class NotebookSoppedEvent(Event):
    type = event_types.NOTEBOOK_STOPPED


auditor.register(NotebookStartedEvent)
auditor.register(NotebookSoppedEvent)
