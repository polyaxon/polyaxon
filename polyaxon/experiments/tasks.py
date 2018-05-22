import logging

from django.db.models import Count

from models.experiments import Experiment, ExperimentMetric
from statuses.experiments import ExperimentLifeCycle
from polyaxon.celery_api import app as celery_app
from polyaxon.settings import CeleryTasks

logger = logging.getLogger('polyaxon.tasks.experiments')


@celery_app.task(name=CeleryTasks.EXPERIMENTS_CHECK_STATUS, ignore_result=True)
def check_experiment_status(experiment_uuid):
    experiment = Experiment.objects.get(uuid=experiment_uuid)
    experiment.update_status()


@celery_app.task(name=CeleryTasks.EXPERIMENTS_SET_METRICS, ignore_result=True)
def set_metrics(experiment_uuid, metrics, created_at=None):
    try:
        experiment = Experiment.objects.get(uuid=experiment_uuid)
    except Experiment.DoesNotExist:
        logger.info('Experiment uuid `%s` does not exist', experiment_uuid)
        return None

    kwargs = {}
    if created_at:
        kwargs['created_at'] = created_at
    ExperimentMetric.objects.create(experiment=experiment, values=metrics, **kwargs)


@celery_app.task(name=CeleryTasks.EXPERIMENTS_SYNC_JOBS_STATUSES, ignore_result=True)
def sync_experiments_and_jobs_statuses():
    experiments = Experiment.objects.exclude(
        experiment_status__status__in=ExperimentLifeCycle.DONE_STATUS)
    experiments = experiments.annotate(num_jobs=Count('jobs')).filter(num_jobs__gt=0)
    for experiment in experiments:
        check_experiment_status.delay(experiment_uuid=experiment.uuid.hex)
