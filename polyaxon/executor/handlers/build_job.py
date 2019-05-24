import conf

from db.redis.tll import RedisTTL
from events import event_subjects
from events.registry import build_job
from events.registry.build_job import BUILD_JOB_FAILED, BUILD_JOB_SUCCEEDED
from executor.handlers.base import BaseHandler
from options.registry.scheduler import SCHEDULER_GLOBAL_COUNTDOWN
from polyaxon.celery_api import celery_app
from polyaxon.settings import SchedulerCeleryTasks


class BuildJobHandler(BaseHandler):
    SUBJECT = event_subjects.BUILD_JOB

    @classmethod
    def _handle_build_job_cleaned_triggered(cls, event: 'Event') -> None:
        instance = event.instance
        if not instance.is_managed:
            return
        if not instance or not instance.has_specification or not instance.is_stoppable:
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
                'is_managed': instance.is_managed,
            },
            countdown=conf.get(SCHEDULER_GLOBAL_COUNTDOWN))

    @classmethod
    def _handle_build_job_post_run(cls, event: 'Event') -> None:
        instance = event.instance
        if not instance.is_managed:
            return
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
                'is_managed': instance.is_managed,
            },
            countdown=RedisTTL.get_for_build(build_id=instance.id))

    @classmethod
    def _handle_build_job_done(cls, event: 'Event') -> None:
        instance = event.instance
        if not instance:
            return

        celery_app.send_task(
            SchedulerCeleryTasks.BUILD_JOBS_NOTIFY_DONE,
            kwargs={'build_job_id': instance.id},
            countdown=conf.get(SCHEDULER_GLOBAL_COUNTDOWN))

    @classmethod
    def record_event(cls, event: 'Event') -> None:
        if event.event_type == build_job.BUILD_JOB_CLEANED_TRIGGERED:
            cls._handle_build_job_cleaned_triggered(event=event)
        elif event.event_type in {BUILD_JOB_FAILED, BUILD_JOB_SUCCEEDED}:
            cls._handle_build_job_post_run(event=event)
        if event.event_type == build_job.BUILD_JOB_DONE:
            cls._handle_build_job_done(event=event)
