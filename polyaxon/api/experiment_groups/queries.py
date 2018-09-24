from django.db.models import Count, Q

from constants.experiments import ExperimentLifeCycle
from db.models.experiment_groups import ExperimentGroup

groups = ExperimentGroup.objects.select_related(
    'user',
    'project',
    'project__user',
    'status',
)

groups_details = groups.annotate(
    Count('experiments', distinct=True),
    Count('iterations', distinct=True),
    pending_experiments__count=Count(
        'experiments',
        filter=Q(experiments__status__status__in=ExperimentLifeCycle.PENDING_STATUS),
        distinct=True),
    running_experiments__count=Count(
        'experiments',
        filter=Q(experiments__status__status__in=ExperimentLifeCycle.RUNNING_STATUS),
        distinct=True),
    scheduled_experiments__count=Count(
        'experiments',
        filter=Q(experiments__status__status=ExperimentLifeCycle.SCHEDULED),
        distinct=True),
    succeeded_experiments__count=Count(
        'experiments',
        filter=Q(experiments__status__status=ExperimentLifeCycle.SUCCEEDED),
        distinct=True),
    failed_experiments__count=Count(
        'experiments',
        filter=Q(experiments__status__status=ExperimentLifeCycle.FAILED),
        distinct=True),
    stopped_experiments__count=Count(
        'experiments',
        filter=Q(experiments__status__status=ExperimentLifeCycle.STOPPED),
        distinct=True),
)
