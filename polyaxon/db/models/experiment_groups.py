import functools
import logging
import uuid

from operator import __or__ as OR

from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.contrib.postgres.fields.jsonb import KeyTransform
from django.db import models
from django.db.models import Q
from django.utils.functional import cached_property

from constants.experiment_groups import ExperimentGroupLifeCycle
from constants.experiments import ExperimentLifeCycle
from db.models.utils import DescribableModel, DiffModel, LastStatusMixin, NameableModel, StatusModel
from libs.spec_validation import validate_group_hptuning_config, validate_group_spec_content
from polyaxon_schemas.hptuning import HPTuningConfig
from polyaxon_schemas.polyaxonfile.specification import GroupSpecification
from polyaxon_schemas.utils import Optimization

_logger = logging.getLogger('polyaxon.db.experiment_groups')


class ExperimentGroup(DiffModel, NameableModel, DescribableModel, LastStatusMixin):
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

    def __str__(self):
        return self.unique_name

    @property
    def unique_name(self):
        return '{}.{}'.format(self.project.unique_name, self.id)

    @property
    def last_status(self):
        return self.status.status if self.status else None

    @property
    def finished_at(self):
        status = self.statuses.filter(status__in=ExperimentGroupLifeCycle.DONE_STATUS).first()
        if status:
            return status.created_at
        return None

    @property
    def started_at(self):
        status = self.statuses.filter(status=ExperimentGroupLifeCycle.RUNNING).first()
        if status:
            return status.created_at
        return None

    def can_transition(self, status):
        """Update the status of the current instance.

        Returns:
            boolean: if the instance is updated.
        """
        if not self.STATUSES.can_transition(status_from=self.last_status, status_to=status):
            _logger.info(
                '`%s` tried to transition from status `%s` to non permitted status `%s`',
                str(self), self.last_status, status)
            return False

        return True

    def set_status(self, status, message=None, **kwargs):
        if not self.can_transition(status):
            return

        ExperimentGroupStatus.objects.create(experiment_group=self, status=status, message=message)

    @cached_property
    def hptuning_config(self):
        return HPTuningConfig.from_dict(self.hptuning) if self.hptuning else None

    @cached_property
    def specification(self):
        return GroupSpecification.read(self.content) if self.content else None

    @cached_property
    def concurrency(self):
        if not self.hptuning_config:
            return None
        return self.hptuning_config.concurrency

    @cached_property
    def search_algorithm(self):
        if not self.hptuning_config:
            return None
        return self.hptuning_config.search_algorithm

    @cached_property
    def has_early_stopping(self):
        return bool(self.early_stopping)

    @cached_property
    def early_stopping(self):
        if not self.hptuning_config:
            return None
        return self.hptuning_config.early_stopping or []

    @property
    def scheduled_experiments(self):
        return self.experiments.filter(
            status__status=ExperimentLifeCycle.SCHEDULED).distinct()

    @property
    def succeeded_experiments(self):
        return self.experiments.filter(
            status__status=ExperimentLifeCycle.SUCCEEDED).distinct()

    @property
    def failed_experiments(self):
        return self.experiments.filter(
            status__status=ExperimentLifeCycle.FAILED).distinct()

    @property
    def stopped_experiments(self):
        return self.experiments.filter(
            status__status=ExperimentLifeCycle.STOPPED).distinct()

    @property
    def pending_experiments(self):
        return self.experiments.filter(
            status__status__in=ExperimentLifeCycle.PENDING_STATUS).distinct()

    @property
    def running_experiments(self):
        return self.experiments.filter(
            status__status__in=ExperimentLifeCycle.RUNNING_STATUS).distinct()

    @property
    def done_experiments(self):
        return self.experiments.filter(
            status__status__in=ExperimentLifeCycle.DONE_STATUS).distinct()

    @property
    def non_done_experiments(self):
        return self.experiments.exclude(
            status__status__in=ExperimentLifeCycle.DONE_STATUS).distinct()

    @property
    def n_experiments_to_start(self):
        """We need to check if we are allowed to start the experiment
        If the polyaxonfile has concurrency we need to check how many experiments are running.
        """
        return self.concurrency - self.running_experiments.count()

    @property
    def iteration(self):
        return self.iterations.last()

    @property
    def iteration_data(self):
        return self.iteration.data if self.iteration else None

    @property
    def current_iteration(self):
        return self.iterations.count()

    def should_stop_early(self):
        filters = []
        for early_stopping_metric in self.early_stopping:
            comparison = (
                'gte' if Optimization.maximize(early_stopping_metric.optimization) else 'lte')
            metric_filter = 'metric__values__{}__{}'.format(
                early_stopping_metric.metric, comparison)
            filters.append({metric_filter: early_stopping_metric.value})
        if filters:
            return self.experiments.filter(functools.reduce(OR, [Q(**f) for f in filters])).exists()
        return False

    def get_annotated_experiments_with_metric(self, metric, experiment_ids=None):
        query = self.experiments
        if experiment_ids:
            query = query.filter(id__in=experiment_ids)
        annotation = {
            metric: KeyTransform(metric, 'metric__values')
        }
        return query.annotate(**annotation)

    def get_ordered_experiments_by_metric(self, experiment_ids, metric, optimization):
        query = self.get_annotated_experiments_with_metric(
            metric=metric,
            experiment_ids=experiment_ids)

        metric_order_by = '{}{}'.format(
            '-' if Optimization.maximize(optimization) else '',
            metric)
        return query.order_by(metric_order_by)

    def get_experiments_metrics(self, metric, experiment_ids=None):
        query = self.get_annotated_experiments_with_metric(
            metric=metric,
            experiment_ids=experiment_ids)
        return query.values_list('id', metric)

    @cached_property
    def search_manager(self):
        from hpsearch.search_managers import get_search_algorithm_manager

        return get_search_algorithm_manager(hptuning_config=self.hptuning_config)

    @cached_property
    def iteration_manager(self):
        from hpsearch.iteration_managers import get_search_iteration_manager

        return get_search_iteration_manager(experiment_group=self)

    @property
    def iteration_config(self):
        from hpsearch.schemas import get_iteration_config

        if self.iteration_data and self.search_algorithm:
            return get_iteration_config(
                search_algorithm=self.search_algorithm,
                iteration=self.iteration_data)
        return None

    def get_suggestions(self):
        iteration_config = self.iteration_config
        if iteration_config:
            return self.search_manager.get_suggestions(iteration_config=iteration_config)
        return self.search_manager.get_suggestions()


class ExperimentGroupIteration(DiffModel):
    experiment_group = models.ForeignKey(
        'db.ExperimentGroup',
        on_delete=models.CASCADE,
        related_name='iterations',
        help_text='The experiment group.')
    data = JSONField(
        help_text='The experiment group iteration meta data.')

    class Meta:
        app_label = 'db'
        ordering = ['created_at']

    def __str__(self):
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
        verbose_name_plural = 'Experiment group Statuses'

    def __str__(self):
        return '{} <{}>'.format(self.experiment_group.unique_name, self.status)
