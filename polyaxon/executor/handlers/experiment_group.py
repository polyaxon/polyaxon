import workers

from events import event_subjects
from events.registry import experiment_group
from executor.handlers.base import BaseHandler
from lifecycles.experiments import ExperimentLifeCycle
from polyaxon.settings import SchedulerCeleryTasks


class ExperimentGroupHandler(BaseHandler):
    SUBJECT = event_subjects.EXPERIMENT_GROUP

    @classmethod
    def _handle_experiment_group_created(cls, event: 'Event') -> None:
        if not event.data['is_managed']:
            return
        if not event.data['has_specification'] or not event.data['is_study']:
            return
        workers.send(
            SchedulerCeleryTasks.EXPERIMENTS_GROUP_CREATE,
            kwargs={'experiment_group_id': event.data['id']})

    @classmethod
    def _handle_experiment_group_done(cls, event: 'Event') -> None:
        instance = event.instance
        if not instance:
            return

        experiments = instance.all_experiments.exclude(
            status__status__in=ExperimentLifeCycle.DONE_STATUS).distinct()
        for experiment in experiments:
            if experiment.is_stoppable:
                workers.send(
                    SchedulerCeleryTasks.EXPERIMENTS_STOP,
                    kwargs={
                        'project_name': experiment.project.unique_name,
                        'project_uuid': experiment.project.uuid.hex,
                        'experiment_name': experiment.unique_name,
                        'experiment_uuid': experiment.uuid.hex,
                        'experiment_group_name': instance.unique_name,
                        'experiment_group_uuid': instance.uuid.hex,
                        'specification': experiment.content,
                        'update_status': True,
                        'collect_logs': True,
                        'is_managed': experiment.is_managed,
                    })

    @classmethod
    def record_event(cls, event: 'Event') -> None:
        if event.event_type == experiment_group.EXPERIMENT_GROUP_CREATED:
            cls._handle_experiment_group_created(event=event)
        elif event.event_type in experiment_group.EXPERIMENT_GROUP_DONE:
            cls._handle_experiment_group_done(event=event)
