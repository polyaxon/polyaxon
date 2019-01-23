from db.redis.tll import RedisTTL
from event_manager import event_subjects
from event_manager.events import build_job
from event_manager.events.build_job import BUILD_JOB_SUCCEEDED, BUILD_JOB_FAILED
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
    def _handle_build_job_post_run(cls, event):
        instance = event.instance
        if not instance or not instance.has_specification:
            return

        celery_app.send_task(
            SchedulerCeleryTasks.BUILD_JOBS_STOP,
            kwargs={
                'project_name': instance.project.unique_name,
                'project_uuid': instance.project.uuid.hex,
                'build_job_name': instance.unique_name,
                'build_job_uuid': instance.uuid.hex,
                'update_status': False,
                'collect_logs': True,
            },
            countdown=RedisTTL.get_for_build(build_id=instance.id))

    @classmethod
    def _handle_build_job_done(cls, event):
        instance = event.instance
        if not instance:
            return

        celery_app.send_task(
            SchedulerCeleryTasks.BUILD_JOBS_NOTIFY_DONE,
            kwargs={'build_job_id': instance.id})

    @classmethod
    def record_event(cls, event):
        if event.event_type == build_job.BUILD_JOB_CLEANED_TRIGGERED:
            cls._handle_build_job_cleaned_triggered(event=event)
        elif event.event_type in {BUILD_JOB_FAILED, BUILD_JOB_SUCCEEDED}:
            cls._handle_build_job_post_run(event=event)
        if event.event_type == build_job.BUILD_JOB_DONE:
            cls._handle_build_job_done(event=event)
