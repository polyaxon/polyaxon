import tracker

from event_manager.events import notebook

tracker.subscribe(notebook.NotebookStartedEvent)
tracker.subscribe(notebook.NotebookStartedTriggeredEvent)
tracker.subscribe(notebook.NotebookSoppedEvent)
tracker.subscribe(notebook.NotebookSoppedTriggeredEvent)
tracker.subscribe(notebook.NotebookViewedEvent)
tracker.subscribe(notebook.NotebookNewStatusEvent)
tracker.subscribe(notebook.NotebookFailedEvent)
tracker.subscribe(notebook.NotebookSucceededEvent)
