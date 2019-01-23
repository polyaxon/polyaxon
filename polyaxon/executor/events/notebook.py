import executor

from event_manager.events import notebook

executor.subscribe(notebook.NotebookStartedEvent)
executor.subscribe(notebook.NotebookSoppedEvent)
executor.subscribe(notebook.NotebookNewStatusEvent)
executor.subscribe(notebook.NotebookFailedEvent)
executor.subscribe(notebook.NotebookSucceededEvent)
