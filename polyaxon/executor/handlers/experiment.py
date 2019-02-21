import conf

from db.redis.tll import RedisTTL
from event_manager import event_subjects
from event_manager.events import experiment
from executor.handlers.base import BaseHandler
from polyaxon.celery_api import celery_app
from polyaxon.settings import HPCeleryTasks, LogsCeleryTasks, SchedulerCeleryTasks


class ExperimentHandler(BaseHandler):
    SUBJECT = event_subjects.EXPERIMENT

    @classmethod
    def _handle_experiment_created(cls, event: 'Event') -> None:
        if event.data['has_specification'] and (event.data['is_independent'] or
                                                event.data['is_clone']):
            # Start building the experiment and then Schedule it to be picked by the spawners
            celery_app.send_task(
                SchedulerCeleryTasks.EXPERIMENTS_BUILD,
                kwargs={'experiment_id': event.data['id']},
                countdown=conf.get('GLOBAL_COUNTDOWN'))

    @classmethod
    def _handle_experiment_cleaned_triggered(cls, event: 'Event') -> None:
        from db.models.experiment_groups import ExperimentGroup

        instance = event.instance
        if not instance or not instance.has_specification or not instance.is_stoppable:
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
                countdown=conf.get('GLOBAL_COUNTDOWN'))
        except ExperimentGroup.DoesNotExist:
            # The experiment was already stopped when the group was deleted
            pass

    @classmethod
    def _handle_experiment_post_run(cls, event: 'Event') -> None:
        instance = event.instance
        if not instance or not instance.has_specification or not instance.jobs.count() > 0:
            return

        # Schedule stop for this experiment because other jobs may be still running
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
                'collect_logs': True,
            },
            countdown=RedisTTL.get_for_experiment(experiment_id=instance.id))

    @classmethod
    def _handle_experiment_done(cls, event: 'Event') -> None:
        instance = event.instance
        if not instance:
            return

        # Check if it's part of an experiment group, and start following tasks
        if not instance.is_independent and not instance.experiment_group.is_stopping:
            celery_app.send_task(
                HPCeleryTasks.HP_START,
                kwargs={'experiment_group_id': instance.experiment_group.id},
                countdown=1)

        # Collect tracked remote logs
        if instance.in_cluster:
            celery_app.send_task(
                LogsCeleryTasks.LOGS_HANDLE_EXPERIMENT_JOB,
                kwargs={
                    'experiment_name': instance.unique_name,
                    'experiment_uuid': instance.uuid.hex,
                    'log_lines': '',
                    'temp': False
                })

    @classmethod
    def record_event(cls, event: 'Event') -> None:
        if event.event_type == experiment.EXPERIMENT_CREATED:
            cls._handle_experiment_created(event=event)
        elif event.event_type == experiment.EXPERIMENT_CLEANED_TRIGGERED:
            cls._handle_experiment_cleaned_triggered(event=event)
        elif event.event_type in {experiment.EXPERIMENT_SUCCEEDED, experiment.EXPERIMENT_FAILED}:
            cls._handle_experiment_post_run(event=event)
        elif event.event_type == experiment.EXPERIMENT_DONE:
            cls._handle_experiment_done(event=event)
