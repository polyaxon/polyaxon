import tracker
from event_manager.events import notebook

tracker.subscribe(notebook.NotebookStartedEvent)
tracker.subscribe(notebook.NotebookSoppedEvent)
tracker.subscribe(notebook.NotebookViewedEvent)
tracker.subscribe(notebook.NotebookNewStatusEvent)
