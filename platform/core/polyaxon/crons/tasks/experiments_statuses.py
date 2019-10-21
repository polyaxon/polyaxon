from django.db.models import Count

import workers

from db.models.experiments import Experiment
from lifecycles.experiments import ExperimentLifeCycle
from polyaxon.settings import CronsCeleryTasks, SchedulerCeleryTasks


@workers.app.task(name=CronsCeleryTasks.EXPERIMENTS_SYNC_JOBS_STATUSES, ignore_result=True)
def experiments_sync_jobs_statuses() -> None:
    experiments = Experiment.objects.exclude(
        status__status__in=ExperimentLifeCycle.DONE_STATUS)
    experiments = experiments.annotate(num_jobs=Count('jobs')).filter(num_jobs__gt=0)
    for experiment in experiments:
        workers.send(
            SchedulerCeleryTasks.EXPERIMENTS_CHECK_STATUS,
            kwargs={'experiment_id': experiment.id})
