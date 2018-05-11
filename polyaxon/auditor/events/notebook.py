import auditor

from event_manager.events import notebook

auditor.subscribe(notebook.NotebookStartedEvent)
auditor.subscribe(notebook.NotebookStartedTriggeredEvent)
auditor.subscribe(notebook.NotebookSoppedEvent)
auditor.subscribe(notebook.NotebookSoppedTriggeredEvent)
auditor.subscribe(notebook.NotebookViewedEvent)
auditor.subscribe(notebook.NotebookNewStatusEvent)
auditor.subscribe(notebook.NotebookFailedEvent)
auditor.subscribe(notebook.NotebookSucceededEvent)
