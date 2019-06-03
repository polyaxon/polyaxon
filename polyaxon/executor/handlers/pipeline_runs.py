import workers

from events import event_subjects
from events.registry import pipeline_run
from executor.handlers.base import BaseHandler
from polyaxon.settings import PipelinesCeleryTasks


class PipelineRunHandler(BaseHandler):
    SUBJECT = event_subjects.PIPELINE_RUN

    @classmethod
    def _handle_pipeline_run_stopped(cls, event: 'Event') -> None:
        instance = event.instance
        if not instance:
            return

        # Schedule stop for this experiment because other jobs may be still running
        workers.send(
            PipelinesCeleryTasks.PIPELINES_STOP_OPERATIONS,
            kwargs={'pipeline_run_id': instance.id,
                    'message': 'Pipeline run was stopped'},
            countdown=None)

    @classmethod
    def _handle_pipeline_run_skipped(cls, event: 'Event') -> None:
        instance = event.instance
        if not instance:
            return

        workers.send(
            PipelinesCeleryTasks.PIPELINES_SKIP_OPERATIONS,
            kwargs={'pipeline_run_id': instance.id,
                    'message': 'Pipeline run was skipped'},
            countdown=None)

    @classmethod
    def record_event(cls, event: 'Event') -> None:
        if event.event_type == pipeline_run.PIPELINE_RUN_STOPPED:
            cls._handle_pipeline_run_stopped(event=event)
        elif event.event_type == pipeline_run.PIPELINE_RUN_SKIPPED:
            cls._handle_pipeline_run_skipped(event=event)
