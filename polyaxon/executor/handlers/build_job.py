from event_manager import event_subjects
from executor.handlers.base import BaseHandler


class BuildJobHandler(BaseHandler):
    SUBJECT = event_subjects.BUILD_JOB
