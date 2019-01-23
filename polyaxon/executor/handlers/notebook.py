from event_manager import event_subjects
from executor.handlers.base import BaseHandler


class NotebookHandler(BaseHandler):
    SUBJECT = event_subjects.NOTEBOOK
