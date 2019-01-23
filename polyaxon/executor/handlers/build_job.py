from event_manager import event_subjects
from event_manager.events import build_job
from executor.handlers.base import BaseHandler
from polyaxon.celery_api import celery_app
from polyaxon.settings import SchedulerCeleryTasks


class BuildJobHandler(BaseHandler):
    SUBJECT = event_subjects.BUILD_JOB

    @classmethod
    def _handle_build_job_cleaned_triggered(cls, event):
        instance = event.instance
        if not instance or not instance.has_specification or not instance.is_running:
            return

        celery_app.send_task(
            SchedulerCeleryTasks.BUILD_JOBS_STOP,
            kwargs={
                'project_name': instance.project.unique_name,
                'project_uuid': instance.project.uuid.hex,
                'build_job_name': instance.unique_name,
                'build_job_uuid': instance.uuid.hex,
                'update_status': False,
                'collect_logs': False,
            })

    @classmethod
    def record_event(cls, event):
        if event.event_type == build_job.BUILD_JOB_CLEANED_TRIGGERED:
            cls._handle_build_job_cleaned_triggered(event=event)
