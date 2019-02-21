import conf

from event_manager import event_subjects
from event_manager.events import notebook
from executor.handlers.base import BaseHandler
from polyaxon.celery_api import celery_app
from polyaxon.settings import SchedulerCeleryTasks


class NotebookHandler(BaseHandler):
    SUBJECT = event_subjects.NOTEBOOK

    @classmethod
    def _handle_notebook_cleaned_triggered(cls, event: 'Event') -> None:
        instance = event.instance
        if not instance or not instance.has_specification or not instance.is_stoppable:
            return

        celery_app.send_task(
            SchedulerCeleryTasks.PROJECTS_NOTEBOOK_STOP,
            kwargs={
                'project_name': instance.project.unique_name,
                'project_uuid': instance.project.uuid.hex,
                'notebook_job_name': instance.unique_name,
                'notebook_job_uuid': instance.uuid.hex,
                'update_status': False,
                'collect_logs': False,
            },
            countdown=conf.get('GLOBAL_COUNTDOWN'))

    @classmethod
    def _handle_notebook_post_run(cls, event: 'Event') -> None:
        instance = event.instance
        if not instance or not instance.has_specification:
            return

        celery_app.send_task(
            SchedulerCeleryTasks.PROJECTS_NOTEBOOK_STOP,
            kwargs={
                'project_name': instance.project.unique_name,
                'project_uuid': instance.project.uuid.hex,
                'notebook_job_name': instance.unique_name,
                'notebook_job_uuid': instance.uuid.hex,
                'update_status': False,
                'collect_logs': True,
            },
            countdown=conf.get('GLOBAL_COUNTDOWN'))

    @classmethod
    def record_event(cls, event: 'Event') -> None:
        if event.event_type == notebook.NOTEBOOK_CLEANED_TRIGGERED:
            cls._handle_notebook_cleaned_triggered(event=event)
        if event.event_type in {notebook.NOTEBOOK_FAILED, notebook.NOTEBOOK_SUCCEEDED}:
            cls._handle_notebook_post_run(event=event)
