import activitylogs

from event_manager.events import notebook

activitylogs.subscribe(notebook.NotebookStartedEvent)
activitylogs.subscribe(notebook.NotebookSoppedEvent)
activitylogs.subscribe(notebook.NotebookViewedEvent)
