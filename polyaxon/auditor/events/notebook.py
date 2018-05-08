import auditor
from event_manager.events import notebook

auditor.register(notebook.NotebookStartedEvent)
auditor.register(notebook.NotebookSoppedEvent)
auditor.register(notebook.NotebookViewedEvent)
auditor.register(notebook.NotebookNewStatusEvent)
