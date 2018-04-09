import functools
import uuid

from operator import __or__ as OR

from django.conf import settings
from django.db import models
from django.db.models import Q
from django.utils.functional import cached_property

from experiment_groups import search_algorithms
from libs.models import DescribableModel, DiffModel
from libs.spec_validation import validate_group_spec_content
from polyaxon_schemas.polyaxonfile.specification import GroupSpecification
from polyaxon_schemas.utils import Optimization
from projects.models import Project
from spawners.utils.constants import ExperimentLifeCycle


class ExperimentGroup(DiffModel, DescribableModel):
    """A model that saves Specification/Polyaxonfiles."""
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        null=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='experiment_groups')
    sequence = models.PositiveSmallIntegerField(
        editable=False,
        null=False,
        help_text='The sequence number of this group within the project.', )
    content = models.TextField(
        help_text='The yaml content of the polyaxonfile/specification.',
        validators=[validate_group_spec_content])
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='experiment_groups',
        help_text='The project this polyaxonfile belongs to.')
    code_reference = models.ForeignKey(
        'repos.CodeReference',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='groups')

    class Meta:
        ordering = ['sequence']
        unique_together = (('project', 'sequence'),)

    def save(self, *args, **kwargs):
        if self.pk is None:
            last = ExperimentGroup.objects.filter(project=self.project).last()
            self.sequence = 1
            if last:
                self.sequence = last.sequence + 1

        super(ExperimentGroup, self).save(*args, **kwargs)

    def __str__(self):
        return self.unique_name

    @property
    def unique_name(self):
        return '{}.{}'.format(self.project.unique_name, self.sequence)

    @cached_property
    def specification(self):
        return GroupSpecification.read(self.content)

    @cached_property
    def concurrency(self):
        if self.specification.settings:
            return self.specification.settings.concurrent_experiments
        return 1

    @cached_property
    def search_algorithm(self):
        if self.specification.settings:
            return self.specification.settings.search_algorithm
        return None

    @property
    def scheduled_experiments(self):
        return self.experiments.filter(
            experiment_status__status=ExperimentLifeCycle.SCHEDULED).distinct()

    @property
    def succeeded_experiments(self):
        return self.experiments.filter(
            experiment_status__status=ExperimentLifeCycle.SUCCEEDED).distinct()

    @property
    def failed_experiments(self):
        return self.experiments.filter(
            experiment_status__status=ExperimentLifeCycle.FAILED).distinct()

    @property
    def stopped_experiments(self):
        return self.experiments.filter(
            experiment_status__status=ExperimentLifeCycle.STOPPED).distinct()

    @property
    def pending_experiments(self):
        return self.experiments.filter(
            experiment_status__status=ExperimentLifeCycle.CREATED).distinct()

    @property
    def running_experiments(self):
        return self.experiments.filter(
            experiment_status__status__in=ExperimentLifeCycle.RUNNING_STATUS).distinct()

    @property
    def n_experiments_to_start(self):
        """We need to check if we are allowed to start the experiment
        If the polyaxonfile has concurrency we need to check how many experiments are running.
        """
        return self.concurrency - self.running_experiments.count()

    def should_stop_early(self):
        filters = []
        for early_stopping_metric in self.specification.early_stopping:
            comparison = (
                'gte' if Optimization.maximize(early_stopping_metric.optimization) else 'lte')
            metric_filter = 'experiment_metric__values__{}__{}'.format(
                early_stopping_metric.metric, comparison)
            filters.append({metric_filter: early_stopping_metric.value})
        if filters:
            return self.experiments.filter(functools.reduce(OR, [Q(**f) for f in filters])).exists()
        return False

    def should_reschedule(self):
        return False

    def get_suggestions(self, iteration=0):
        search_algorithm = search_algorithms.get_search_algorithm(specification=self.specification)
        return search_algorithm.get_suggestions()
