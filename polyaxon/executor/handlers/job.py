from event_manager import event_subjects
from event_manager.events import job
from executor.handlers.base import BaseHandler
from polyaxon.celery_api import celery_app
from polyaxon.settings import SchedulerCeleryTasks


class JobHandler(BaseHandler):
    SUBJECT = event_subjects.JOB

    @classmethod
    def _handle_job_created(cls, event):
        if not event.data['has_specification']:
            return

        # Start building the job and then Schedule it to be picked by the spawners
        celery_app.send_task(
            SchedulerCeleryTasks.JOBS_BUILD,
            kwargs={'job_id': event.data['id']},
            countdown=1)

    @classmethod
    def _handle_job_cleaned_triggered(cls, event):
        instance = event.instance
        if not instance or not instance.has_specification or not instance.is_running:
            return

        celery_app.send_task(
            SchedulerCeleryTasks.JOBS_STOP,
            kwargs={
                'project_name': instance.project.unique_name,
                'project_uuid': instance.project.uuid.hex,
                'job_name': instance.unique_name,
                'job_uuid': instance.uuid.hex,
                'update_status': False,
                'collect_logs': False,
            })

    @classmethod
    def record_event(cls, event):
        if event.event_type == job.JOB_CREATED:
            cls._handle_job_created(event=event)
        elif event.event_type == job.JOB_CLEANED_TRIGGERED:
            cls._handle_job_cleaned_triggered(event=event)
