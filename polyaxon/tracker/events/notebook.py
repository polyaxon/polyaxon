import tracker

from event_manager.events import notebook

tracker.subscribe(notebook.NotebookStartedEvent)
tracker.subscribe(notebook.NotebookStartedTriggeredEvent)
tracker.subscribe(notebook.NotebookSoppedEvent)
tracker.subscribe(notebook.NotebookSoppedTriggeredEvent)
tracker.subscribe(notebook.NotebookViewedEvent)
tracker.subscribe(notebook.NotebookUpdatedEvent)
tracker.subscribe(notebook.NotebookDeletedEvent)
tracker.subscribe(notebook.NotebookDeletedTriggeredEvent)
tracker.subscribe(notebook.NotebookNewStatusEvent)
tracker.subscribe(notebook.NotebookFailedEvent)
tracker.subscribe(notebook.NotebookSucceededEvent)
tracker.subscribe(notebook.NotebookStatusesViewedEvent)
tracker.subscribe(notebook.NotebookArchivedEvent)
tracker.subscribe(notebook.NotebookRestoredEvent)
