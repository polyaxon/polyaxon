import analytics
from event_manager.events import notebook

analytics.subscribe(notebook.NotebookStartedEvent)
analytics.subscribe(notebook.NotebookSoppedEvent)
analytics.subscribe(notebook.NotebookViewedEvent)
analytics.subscribe(notebook.NotebookNewStatusEvent)
