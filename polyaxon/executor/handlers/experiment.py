from event_manager import event_subjects
from event_manager.events import experiment
from executor.handlers.base import BaseHandler
from polyaxon.celery_api import celery_app
from polyaxon.settings import SchedulerCeleryTasks


class ExperimentHandler(BaseHandler):
    SUBJECT = event_subjects.EXPERIMENT

    @classmethod
    def _handle_experiment_created(cls, event):
        if event.data['has_specification'] and (event.data['is_independent'] or
                                                event.data['is_clone']):
            # Start building the experiment and then Schedule it to be picked by the spawners
            celery_app.send_task(
                SchedulerCeleryTasks.EXPERIMENTS_BUILD,
                kwargs={'experiment_id': event.data['id']},
                countdown=1)

    @classmethod
    def record_event(cls, event):
        if event.event_type == experiment.EXPERIMENT_CREATED:
            cls._handle_experiment_created(event=event)
