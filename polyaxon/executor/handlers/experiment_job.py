import conf

from events import event_subjects
from events.registry import experiment_job
from executor.handlers.base import BaseHandler
from lifecycles.jobs import JobLifeCycle
from options.registry.scheduler import SCHEDULER_GLOBAL_COUNTDOWN
from polyaxon.celery_api import celery_app
from polyaxon.settings import SchedulerCeleryTasks


class ExperimentJobHandler(BaseHandler):
    SUBJECT = event_subjects.EXPERIMENT_JOB

    @classmethod
    def _handle_experiment_job_new_status(cls, event: 'Event') -> None:
        instance = event.instance
        cond = (not instance or
                instance.experiment.is_done or
                instance.last_status == JobLifeCycle.CREATED)
        if cond:
            return

        celery_app.send_task(
            SchedulerCeleryTasks.EXPERIMENTS_CHECK_STATUS,
            kwargs={'experiment_id': instance.experiment.id},
            countdown=conf.get(SCHEDULER_GLOBAL_COUNTDOWN))

    @classmethod
    def record_event(cls, event: 'Event') -> None:
        if event.event_type == experiment_job.EXPERIMENT_JOB_NEW_STATUS:
            cls._handle_experiment_job_new_status(event=event)
