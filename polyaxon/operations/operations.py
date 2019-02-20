import conf

from db.getters.experiments import get_valid_experiment
from pipelines.celery_task import ClassBasedTask, OperationRunError
from polyaxon.celery_api import celery_app
from polyaxon.settings import CeleryOperationTasks, SchedulerCeleryTasks


class ScheduleExperimentTask(ClassBasedTask):
    @staticmethod
    def _run(task_bind, *args, **kwargs):
        experiment_id = kwargs['experiment_id']
        experiment = get_valid_experiment(experiment_id=experiment_id)
        if not experiment:
            raise OperationRunError(
                'The Experiment `{}` does not exist anymore.'.format(experiment_id))

        celery_app.send_task(
            SchedulerCeleryTasks.EXPERIMENTS_BUILD,
            kwargs={'experiment_id': experiment_id},
            countdown=conf.get('GLOBAL_COUNTDOWN'))


@celery_app.task(name=CeleryOperationTasks.EXPERIMENTS_SCHEDULE, bind=True, ignore_result=True)
def schedule_experiment(self, experiment_id):
    ScheduleExperimentTask.run(task_bind=self, experiment_id=experiment_id)
