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
    def _handle_experiment_cleaned_triggered(cls, event):
        from db.models.experiment_groups import ExperimentGroup

        instance = event.instance
        if not instance or not instance.has_specification or not instance.is_running:
            return

        if instance.jobs.count() == 0:
            return

        try:
            group = instance.experiment_group
            celery_app.send_task(
                SchedulerCeleryTasks.EXPERIMENTS_STOP,
                kwargs={
                    'project_name': instance.project.unique_name,
                    'project_uuid': instance.project.uuid.hex,
                    'experiment_name': instance.unique_name,
                    'experiment_uuid': instance.uuid.hex,
                    'experiment_group_name': group.unique_name if group else None,
                    'experiment_group_uuid': group.uuid.hex if group else None,
                    'specification': instance.config,
                    'update_status': False,
                    'collect_logs': False,
                },
                countdown=1)
        except ExperimentGroup.DoesNotExist:
            # The experiment was already stopped when the group was deleted
            pass

    @classmethod
    def record_event(cls, event):
        if event.event_type == experiment.EXPERIMENT_CREATED:
            cls._handle_experiment_created(event=event)
        elif event.event_type == experiment.EXPERIMENT_CLEANED_TRIGGERED:
            cls._handle_experiment_cleaned_triggered(event=event)
