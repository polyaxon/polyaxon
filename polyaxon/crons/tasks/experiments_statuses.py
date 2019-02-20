from django.db.models import Count

import conf

from constants.experiments import ExperimentLifeCycle
from db.models.experiments import Experiment
from polyaxon.celery_api import celery_app
from polyaxon.settings import CronsCeleryTasks, SchedulerCeleryTasks


@celery_app.task(name=CronsCeleryTasks.EXPERIMENTS_SYNC_JOBS_STATUSES, ignore_result=True)
def experiments_sync_jobs_statuses() -> None:
    experiments = Experiment.objects.exclude(
        status__status__in=ExperimentLifeCycle.DONE_STATUS)
    experiments = experiments.annotate(num_jobs=Count('jobs')).filter(num_jobs__gt=0)
    for experiment in experiments:
        celery_app.send_task(
            SchedulerCeleryTasks.EXPERIMENTS_CHECK_STATUS,
            kwargs={'experiment_id': experiment.id},
            countdown=conf.get('GLOBAL_COUNTDOWN'))
