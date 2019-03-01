import functools
import logging
import uuid

from operator import __or__ as OR
from typing import Dict, List, Optional

from hestia.datetime_typing import AwareDT

from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.contrib.postgres.fields.jsonb import KeyTransform
from django.db import models
from django.db.models import Q
from django.utils.functional import cached_property

from constants.experiment_groups import ExperimentGroupLifeCycle
from constants.experiments import ExperimentLifeCycle
from db.models.abstract_jobs import TensorboardJobMixin
from db.models.charts import ChartViewModel
from db.models.statuses import LastStatusMixin, StatusModel
from db.models.unique_names import GROUP_UNIQUE_NAME_FORMAT
from db.models.utils import (
    DeletedModel,
    DescribableModel,
    DiffModel,
    NameableModel,
    PersistenceModel,
    ReadmeModel,
    RunTimeModel,
    SubPathModel,
    TagModel
)
from libs.paths.experiment_groups import get_experiment_group_subpath
from libs.spec_validation import validate_group_hptuning_config, validate_group_spec_content
from schemas.hptuning import HPTuningConfig, Optimization
from schemas.specifications import GroupSpecification

_logger = logging.getLogger('polyaxon.db.experiment_groups')


class GroupTypes(object):
    STUDY = 'study'
    SELECTION = 'selection'

    VALUES = {STUDY, SELECTION}
    CHOICES = (
        (STUDY, STUDY),
        (SELECTION, SELECTION)
    )


class ExperimentGroup(DiffModel,
                      RunTimeModel,
                      NameableModel,
                      PersistenceModel,
                      DescribableModel,
                      ReadmeModel,
                      SubPathModel,
                      TagModel,
                      DeletedModel,
                      LastStatusMixin,
                      TensorboardJobMixin):
    """A model that saves Specification/Polyaxonfiles."""
    STATUSES = ExperimentGroupLifeCycle

    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        null=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='+')
    project = models.ForeignKey(
        'db.Project',
        on_delete=models.CASCADE,
        related_name='experiment_groups',
        help_text='The project this polyaxonfile belongs to.')
    group_type = models.CharField(
        max_length=10,
        default=GroupTypes.STUDY,
        choices=GroupTypes.CHOICES)
    selection_experiments = models.ManyToManyField(
        'db.Experiment',
        blank=True,
        related_name='selections'
    )
    content = models.TextField(
        null=True,
        blank=True,
        help_text='The yaml content of the polyaxonfile/specification.',
        validators=[validate_group_spec_content])
    hptuning = JSONField(
        help_text='The experiment group hptuning params config.',
        null=True,
        blank=True,
        validators=[validate_group_hptuning_config])
    code_reference = models.ForeignKey(
        'db.CodeReference',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='+')
    status = models.OneToOneField(
        'db.ExperimentGroupStatus',
        related_name='+',
        blank=True,
        null=True,
        editable=True,
        on_delete=models.SET_NULL)

    class Meta:
        app_label = 'db'
        unique_together = (('project', 'name'),)

    def __str__(self) -> str:
        return self.unique_name

    @property
    def unique_name(self) -> str:
        return GROUP_UNIQUE_NAME_FORMAT.format(
            project_name=self.project.unique_name,
            id=self.id)

    @cached_property
    def subpath(self) -> str:
        return get_experiment_group_subpath(self.unique_name)

    @property
    def is_study(self) -> bool:
        return self.group_type == GroupTypes.STUDY

    @property
    def is_selection(self) -> bool:
        return self.group_type == GroupTypes.SELECTION

    @property
    def is_stopping(self) -> bool:
        return self.last_status == self.STATUSES.STOPPING

    def can_transition(self, status_from, status_to) -> bool:
        """Update the status of the current instance.

        Returns:
            boolean: if the instance is updated.
        """
        if not self.STATUSES.can_transition(status_from=status_from, status_to=status_to):
            _logger.info(
                '`%s` tried to transition from status `%s` to non permitted status `%s`',
                str(self), status_from, status_to)
            return False

        return True

    def last_status_before(self, status_date: AwareDT = None) -> Optional[str]:
        if not status_date:
            return self.last_status
        status = ExperimentGroupStatus.objects.filter(
            experiment_group=self,
            created_at__lte=status_date).last()
        return status.status if status else None

    def set_status(self, status: str,
                   created_at: AwareDT = None,
                   message: str = None,
                   traceback: Dict = None, **kwargs) -> None:
        status_from = self.last_status_before(status_date=created_at)

        if not self.can_transition(status_from=status_from, status_to=status):
            return

        params = {'created_at': created_at} if created_at else {}
        ExperimentGroupStatus.objects.create(experiment_group=self,
                                             status=status,
                                             message=message,
                                             traceback=traceback,
                                             **params)

    def archive(self) -> bool:
        if not super().archive():
            return False
        self.experiments.update(deleted=True)
        return True

    def restore(self) -> bool:
        if not super().restore():
            return False
        self.all_experiments.update(deleted=False)
        return True

    @cached_property
    def hptuning_config(self) -> Optional['HPTuningConfig']:
        return HPTuningConfig.from_dict(self.hptuning) if self.hptuning else None

    @cached_property
    def specification(self) -> Optional['GroupSpecification']:
        return GroupSpecification.read(self.content) if self.content else None

    @property
    def has_specification(self) -> bool:
        return self.content is not None

    @cached_property
    def concurrency(self) -> Optional[int]:
        if not self.hptuning_config:
            return None
        return self.hptuning_config.concurrency

    @cached_property
    def search_algorithm(self) -> Optional[str]:
        if not self.hptuning_config:
            return None
        return self.hptuning_config.search_algorithm

    @cached_property
    def has_early_stopping(self) -> bool:
        return bool(self.early_stopping)

    @cached_property
    def early_stopping(self) -> Optional[List]:
        if not self.hptuning_config:
            return None
        return self.hptuning_config.early_stopping or []

    @property
    def group_experiments(self):
        if self.is_selection:
            return self.selection_experiments
        return self.experiments

    @property
    def all_experiments(self):
        """
        Similar to experiments,
        but uses the default manager to return archived experiments as well.
        """
        from db.models.experiments import Experiment

        return Experiment.all.filter(experiment_group=self)

    @property
    def all_group_experiments(self):
        """
        Similar to group_experiments,
        but uses the default manager to return archived experiments as well.
        """
        from db.models.experiments import Experiment

        if self.is_selection:
            return Experiment.all.filter(selections=self)
        return Experiment.all.filter(experiment_group=self)

    @property
    def scheduled_experiments(self):
        return self.group_experiments.filter(
            status__status=ExperimentLifeCycle.SCHEDULED).distinct()

    @property
    def succeeded_experiments(self):
        return self.group_experiments.filter(
            status__status=ExperimentLifeCycle.SUCCEEDED).distinct()

    @property
    def failed_experiments(self):
        return self.group_experiments.filter(
            status__status=ExperimentLifeCycle.FAILED).distinct()

    @property
    def stopped_experiments(self):
        return self.group_experiments.filter(
            status__status=ExperimentLifeCycle.STOPPED).distinct()

    @property
    def pending_experiments(self):
        return self.group_experiments.filter(
            status__status__in=ExperimentLifeCycle.PENDING_STATUS).distinct()

    @property
    def running_experiments(self):
        return self.group_experiments.filter(
            status__status__in=ExperimentLifeCycle.RUNNING_STATUS).distinct()

    @property
    def k8s_experiments(self):
        scheduled_statuses = (ExperimentLifeCycle.RUNNING_STATUS |
                              {ExperimentLifeCycle.UNKNOWN, ExperimentLifeCycle.WARNING})
        return self.group_experiments.filter(
            status__status__in=scheduled_statuses).distinct()

    @property
    def done_experiments(self):
        return self.group_experiments.filter(
            status__status__in=ExperimentLifeCycle.DONE_STATUS).distinct()

    @property
    def non_done_experiments(self):
        return self.group_experiments.exclude(
            status__status__in=ExperimentLifeCycle.DONE_STATUS).distinct()

    @property
    def n_experiments_to_start(self) -> int:
        """We need to check if we are allowed to start the experiment
        If the polyaxonfile has concurrency we need to check how many experiments are running.
        """
        return self.concurrency - self.k8s_experiments.count()

    @property
    def iteration(self):
        return self.iterations.last()

    @property
    def iteration_data(self):
        data = self.iteration.data if self.iteration else None
        if data:
            data['experiment_ids'] = list(self.iteration.experiments.values_list('id', flat=True))

        return data

    @property
    def current_iteration(self) -> int:
        return self.iterations.count()

    def should_stop_early(self) -> bool:
        filters = []
        for early_stopping_metric in self.early_stopping:
            comparison = (
                'gte' if Optimization.maximize(early_stopping_metric.optimization) else 'lte')
            metric_filter = 'last_metric__{}__{}'.format(
                early_stopping_metric.metric, comparison)
            filters.append({metric_filter: early_stopping_metric.value})
        if filters:
            return self.experiments.filter(functools.reduce(OR, [Q(**f) for f in filters])).exists()
        return False

    def get_annotated_experiments_with_metric(self, metric: str, experiment_ids: List[int] = None):
        query = self.experiments
        if experiment_ids:
            query = query.filter(id__in=experiment_ids)
        annotation = {
            metric: KeyTransform(metric, 'last_metric')
        }
        return query.annotate(**annotation)

    def get_ordered_experiments_by_metric(self,
                                          experiment_ids: List[int],
                                          metric: str,
                                          optimization: str):
        query = self.get_annotated_experiments_with_metric(
            metric=metric,
            experiment_ids=experiment_ids)

        metric_order_by = '{}{}'.format(
            '-' if Optimization.maximize(optimization) else '',
            metric)
        return query.order_by(metric_order_by)

    def get_experiments_metrics(self, metric: str, experiment_ids: List[int] = None):
        query = self.get_annotated_experiments_with_metric(
            metric=metric,
            experiment_ids=experiment_ids)
        return query.values_list('id', metric)

    def get_experiments_declarations(self, experiment_ids: List[int] = None):
        return self.experiments.filter(id__in=experiment_ids).values_list('id', 'declarations')

    @cached_property
    def search_manager(self) -> 'BaseSearchAlgorithmManager':
        from hpsearch.search_managers import get_search_algorithm_manager

        return get_search_algorithm_manager(hptuning_config=self.hptuning_config)

    @cached_property
    def iteration_manager(self) -> 'BaseIterationManager':
        from hpsearch.iteration_managers import get_search_iteration_manager

        return get_search_iteration_manager(experiment_group=self)

    @property
    def iteration_config(self) -> 'BaseIterationConfig':
        from hpsearch.schemas import get_iteration_config

        iteration_data = self.iteration_data

        if iteration_data and self.search_algorithm:
            return get_iteration_config(
                search_algorithm=self.search_algorithm,
                iteration=iteration_data)
        return None

    def get_suggestions(self):
        iteration_config = self.iteration_config
        if iteration_config:
            return self.search_manager.get_suggestions(iteration_config=iteration_config)
        return self.search_manager.get_suggestions()

    def get_num_suggestions(self) -> int:
        iteration_config = self.iteration_config
        return self.search_manager.get_num_suggestions(iteration_config=iteration_config)

    def scheduled_all_suggestions(self):
        iteration_config = self.iteration_config
        return self.search_manager.scheduled_all_suggestions(iteration_config=iteration_config)


class ExperimentGroupIteration(DiffModel):
    experiment_group = models.ForeignKey(
        'db.ExperimentGroup',
        on_delete=models.CASCADE,
        related_name='iterations',
        help_text='The experiment group.')
    experiments = models.ManyToManyField(
        'db.Experiment',
        blank=True,
        related_name='+'
    )
    data = JSONField(
        help_text='The experiment group iteration meta data.')

    class Meta:
        app_label = 'db'
        ordering = ['created_at']

    def __str__(self) -> str:
        return '{} <{}>'.format(self.experiment_group, self.created_at)


class ExperimentGroupStatus(StatusModel):
    """A model that represents an experiment group status at certain time."""
    STATUSES = ExperimentGroupLifeCycle

    experiment_group = models.ForeignKey(
        'db.ExperimentGroup',
        on_delete=models.CASCADE,
        related_name='statuses')
    status = models.CharField(
        max_length=64,
        blank=True,
        null=True,
        default=STATUSES.CREATED,
        choices=STATUSES.CHOICES)

    class Meta:
        app_label = 'db'
        verbose_name_plural = 'Experiment Group Statuses'

    def __str__(self) -> str:
        return '{} <{}>'.format(self.experiment_group.unique_name, self.status)


class ExperimentGroupChartView(ChartViewModel):
    """A model that represents an experiment group chart view."""
    experiment_group = models.ForeignKey(
        'db.ExperimentGroup',
        on_delete=models.CASCADE,
        related_name='chart_views')

    class Meta:
        app_label = 'db'
        verbose_name_plural = 'Experiment Group Chart Views'
        ordering = ['created_at']
