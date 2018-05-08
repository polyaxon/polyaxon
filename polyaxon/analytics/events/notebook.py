import auditor
from libs.event_manager.base_events import notebook

auditor.register(notebook.NotebookStartedEvent)
auditor.register(notebook.NotebookSoppedEvent)
auditor.register(notebook.NotebookNewStatusEvent)
