from django.db.models import Count

from constants.experiments import ExperimentLifeCycle
from db.models.experiments import Experiment
from polyaxon.celery_api import app as celery_app
from polyaxon.settings import CeleryTasks


@celery_app.task(name=CeleryTasks.EXPERIMENTS_SYNC_JOBS_STATUSES, ignore_result=True)
def sync_experiments_and_jobs_statuses():
    experiments = Experiment.objects.exclude(
        experiment_status__status__in=ExperimentLifeCycle.DONE_STATUS)
    experiments = experiments.annotate(num_jobs=Count('jobs')).filter(num_jobs__gt=0)
    for experiment in experiments:
        celery_app.send_task(
            CeleryTasks.EXPERIMENTS_CHECK_STATUS,
            kwargs={'experiment_uuid': experiment.uuid.hex})
