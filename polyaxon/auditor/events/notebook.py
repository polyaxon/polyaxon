import auditor

from event_manager.events import notebook

auditor.subscribe(notebook.NotebookStartedEvent)
auditor.subscribe(notebook.NotebookSoppedEvent)
auditor.subscribe(notebook.NotebookViewedEvent)
auditor.subscribe(notebook.NotebookNewStatusEvent)
