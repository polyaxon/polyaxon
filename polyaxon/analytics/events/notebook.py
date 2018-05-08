import analytics
from event_manager.events import notebook

analytics.register(notebook.NotebookStartedEvent)
analytics.register(notebook.NotebookSoppedEvent)
analytics.register(notebook.NotebookViewedEvent)
analytics.register(notebook.NotebookNewStatusEvent)
