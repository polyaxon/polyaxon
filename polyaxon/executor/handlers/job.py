from event_manager import event_subjects
from event_manager.events import job
from executor.handlers.base import BaseHandler

from polyaxon.celery_api import celery_app
from polyaxon.settings import SchedulerCeleryTasks


class JobHandler(BaseHandler):
    SUBJECT = event_subjects.JOB

    @classmethod
    def _handle_job_created(cls, event):
        if event.data['has_specification']:
            # Start building the job and then Schedule it to be picked by the spawners
            celery_app.send_task(
                SchedulerCeleryTasks.JOBS_BUILD,
                kwargs={'job_id': event.data['id']},
                countdown=1)

    @classmethod
    def record_event(cls, event):
        if event.event_type == job.JOB_CREATED:
            cls._handle_job_created(event=event)
