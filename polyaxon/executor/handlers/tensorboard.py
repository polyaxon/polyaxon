from event_manager import event_subjects
from executor.handlers.base import BaseHandler


class TensorboardHandler(BaseHandler):
    SUBJECT = event_subjects.TENSORBOARD
