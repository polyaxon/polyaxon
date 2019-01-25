from event_manager import event_subjects
from event_manager.events import experiment_group
from executor.handlers.base import BaseHandler
from polyaxon.celery_api import celery_app
from polyaxon.settings import SchedulerCeleryTasks


class ExperimentGroupHandler(BaseHandler):
    SUBJECT = event_subjects.EXPERIMENT_GROUP

    @classmethod
    def _handle_experiment_group_created(cls, event):
        if not event.data['has_specification'] or not event.data['is_study']:
            return
        celery_app.send_task(
            SchedulerCeleryTasks.EXPERIMENTS_GROUP_CREATE,
            kwargs={'experiment_group_id': event.data['id']},
            countdown=1)

    @classmethod
    def record_event(cls, event):
        if event.event_type == experiment_group.EXPERIMENT_GROUP_CREATED:
            cls._handle_experiment_group_created(event=event)
