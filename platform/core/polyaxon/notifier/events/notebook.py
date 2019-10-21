import notifier

from events.registry import notebook

# notifier.subscribe_event(notebook.NotebookNewStatusEvent)
notifier.subscribe_event(notebook.NotebookStartedEvent)
notifier.subscribe_event(notebook.NotebookFailedEvent)
notifier.subscribe_event(notebook.NotebookSucceededEvent)
