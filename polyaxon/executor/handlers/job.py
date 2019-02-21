import conf

from db.redis.tll import RedisTTL
from event_manager import event_subjects
from event_manager.events import job
from event_manager.events.job import JOB_FAILED, JOB_SUCCEEDED
from executor.handlers.base import BaseHandler
from polyaxon.celery_api import celery_app
from polyaxon.settings import SchedulerCeleryTasks


class JobHandler(BaseHandler):
    SUBJECT = event_subjects.JOB

    @classmethod
    def _handle_job_created(cls, event: 'Event') -> None:
        if not event.data['has_specification']:
            return

        # Start building the job and then Schedule it to be picked by the spawners
        celery_app.send_task(
            SchedulerCeleryTasks.JOBS_BUILD,
            kwargs={'job_id': event.data['id']},
            countdown=conf.get('GLOBAL_COUNTDOWN'))

    @classmethod
    def _handle_job_cleaned_triggered(cls, event: 'Event') -> None:
        instance = event.instance
        if not instance or not instance.has_specification or not instance.is_stoppable:
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
            },
            countdown=conf.get('GLOBAL_COUNTDOWN'))

    @classmethod
    def _handle_job_post_run(cls, event: 'Event') -> None:
        instance = event.instance
        if not instance or not instance.has_specification:
            return

        celery_app.send_task(
            SchedulerCeleryTasks.JOBS_STOP,
            kwargs={
                'project_name': instance.project.unique_name,
                'project_uuid': instance.project.uuid.hex,
                'job_name': instance.unique_name,
                'job_uuid': instance.uuid.hex,
                'update_status': False,
                'collect_logs': True,
            },
            countdown=RedisTTL.get_for_job(job_id=instance.id))

    @classmethod
    def record_event(cls, event: 'Event') -> None:
        if event.event_type == job.JOB_CREATED:
            cls._handle_job_created(event=event)
        elif event.event_type == job.JOB_CLEANED_TRIGGERED:
            cls._handle_job_cleaned_triggered(event=event)
        elif event.event_type in {JOB_FAILED, JOB_SUCCEEDED}:
            cls._handle_job_post_run(event=event)
