import logging
import uuid

from typing import Dict, Optional, Tuple

from hestia.datetime_typing import AwareDT

from django.conf import settings
from django.db import models
from django.db.models import Q
from django.dispatch import Signal
from django.utils.functional import cached_property

import compiler

from db.models.abstract.backend import BackendModel
from db.models.abstract.deleted import DeletedModel
from db.models.abstract.describable import DescribableModel
from db.models.abstract.diff import DiffModel
from db.models.abstract.executable import ExecutableModel
from db.models.abstract.is_managed import IsManagedModel
from db.models.abstract.nameable import NameableModel
from db.models.abstract.run import RunModel
from db.models.abstract.tag import TagModel
from db.models.abstract.unique_name import UniqueNameMixin
from db.models.statuses import StatusModel
from db.models.unique_names import PIPELINES_UNIQUE_NAME_FORMAT
from lifecycles.operations import OperationStatuses
from lifecycles.pipelines import PipelineLifeCycle
from schemas import kinds

_logger = logging.getLogger('db.pipelines')

status_change = Signal(providing_args=["instance", "status"])


class Pipeline(DiffModel,
               NameableModel,
               BackendModel,
               IsManagedModel,
               DescribableModel,
               TagModel,
               ExecutableModel,
               DeletedModel,
               UniqueNameMixin):
    """A model that represents a pipeline (DAG - directed acyclic graph).

    A Pipeline is a collection / namespace of operations with directional dependencies.
    A Pipeline can optionally have
     * a schedule (e.g. daily, hourly, ...)
     * a start end an end date

    Every operation has dependencies, and can only run when all the dependencies are met.

    Certain operations can depend on their own past, i.e that they can't run
    until their previous schedule (and upstream operations) are completed.

    A pipeline can also have dependencies/upstream pipelines/operations.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='+')
    project = models.ForeignKey(
        'db.Project',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='pipelines')
    schedule = models.OneToOneField(
        'db.Schedule',
        null=True,
        blank=True,
        on_delete=models.SET_NULL)
    content = models.TextField(
        blank=True,
        null=True,
        help_text='The yaml content of the polyaxonfile/specification.')
    concurrency = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        help_text="If set, it determines the number of operation instances "
                  "allowed to run concurrently.")

    def __str__(self):
        return self.unique_name

    class Meta:
        app_label = 'db'
        unique_together = (('project', 'name'),)
        indexes = [
            models.Index(fields=['name']),
        ]

    @cached_property
    def unique_name(self) -> str:
        return PIPELINES_UNIQUE_NAME_FORMAT.format(
            project_name=self.project.unique_name,
            id=self.id)

    @property
    def has_specification(self) -> bool:
        return self.content is not None

    @cached_property
    def specification(self) -> Optional['PipelineSpecification']:
        return compiler.compile(kind=kinds.PIPELINE, content=self.content)

    @property
    def dag(self) -> Tuple[Dict, Dict]:
        """Construct the DAG of this pipeline based on the its operations and their downstream."""
        from polyflow import dags

        operations = self.operations.all().prefetch_related('downstream_operations')

        def get_downstream(op):
            return op.downstream_operations.values_list('id', flat=True)

        return dags.get_dag(operations, get_downstream)


class PipelineRunStatus(StatusModel):
    """A model that represents a pipeline run status at certain time."""
    STATUSES = PipelineLifeCycle

    status = models.CharField(
        max_length=64,
        blank=True,
        null=True,
        default=STATUSES.CREATED,
        choices=STATUSES.CHOICES)
    pipeline_run = models.ForeignKey(
        'db.PipelineRun',
        on_delete=models.CASCADE,
        related_name='statuses')

    class Meta:
        app_label = 'db'
        verbose_name_plural = 'Pipeline Run Statuses'
        ordering = ['created_at']

    def __str__(self) -> str:
        return '{} <{}>'.format(self.pipeline_run, self.status)


class PipelineRun(RunModel):
    """A model that represents an execution behaviour/run of instance of a pipeline.

    Since this is an instance of known Pipeline,
    we can store the sorted topology of the dag,
    which should should not change during the execution time.
    """
    STATUSES = PipelineLifeCycle

    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        null=False)
    pipeline = models.ForeignKey(
        'db.Pipeline',
        on_delete=models.CASCADE,
        related_name='runs')
    status = models.OneToOneField(
        'db.PipelineRunStatus',
        related_name='+',
        blank=True,
        null=True,
        editable=True,
        on_delete=models.SET_NULL)

    class Meta:
        app_label = 'db'

    @property
    def dag(self) -> Tuple[Dict, Dict]:
        """Construct the DAG of this pipeline run
        based on the its operation runs and their downstream.
        """
        from polyflow import dags

        operation_runs = self.operation_runs.all().prefetch_related('downstream_runs')

        def get_downstream(op_run):
            return op_run.downstream_runs.values_list('id', flat=True)

        return dags.get_dag(operation_runs, get_downstream)

    def on_done(self, message: str = None) -> None:
        self.set_status(status=self.STATUSES.DONE, message=message)

    def last_status_before(self, status_date: AwareDT = None) -> Optional[str]:
        if not status_date:
            return self.last_status
        status = PipelineRunStatus.objects.filter(
            pipeline_run=self,
            created_at__lte=status_date).last()
        return status.status if status else None

    def set_status(self,
                   status: str,
                   created_at: AwareDT = None,
                   message: str = None,
                   traceback: Dict = None,
                   **kwargs) -> None:
        last_status = self.last_status_before(status_date=created_at)
        if not PipelineLifeCycle.can_transition(status_from=last_status, status_to=status):
            return

        if PipelineLifeCycle.DONE != status:
            # If the status that we want to transition to is not a final state,
            # then no further checks are required
            params = {'created_at': created_at} if created_at else {}
            PipelineRunStatus.objects.create(pipeline_run=self,
                                             status=status,
                                             message=message,
                                             traceback=traceback,
                                             **params)
            return

        # If we reached a final state,
        # we mark the pipeline as FINISHED if all operation runs are finished
        all_op_runs_done = not bool([
            True for status in
            self.operation_runs.values_list('status', flat=True)
            if status not in OperationStatuses.DONE_STATUS
        ])
        if all_op_runs_done:
            PipelineRunStatus.objects.create(pipeline_run=self, status=status, message=message)

    def on_scheduled(self, message: str = None) -> None:
        self.set_status(status=PipelineLifeCycle.SCHEDULED, message=message)

    def on_run(self, message: str = None) -> None:
        self.set_status(status=PipelineLifeCycle.RUNNING, message=message)

    def on_timeout(self, message: str = None) -> None:
        self.set_status(status=PipelineLifeCycle.FAILED, message=message)

    def on_stop(self, message: str = None) -> None:
        self.set_status(status=PipelineLifeCycle.STOPPED, message=message)

    def on_skip(self, message: str = None) -> None:
        self.set_status(status=PipelineLifeCycle.SKIPPED, message=message)

    @property
    def skipped(self) -> bool:
        return PipelineLifeCycle.skipped(self.last_status)

    @property
    def running_operation_runs(self):
        return self.operation_runs.exclude(Q(status__in=OperationStatuses.DONE_STATUS) |
                                           Q(status__isnull=True))

    @property
    def n_operation_runs_to_start(self):
        """We need to check if we are allowed to start any operations"""
        return self.pipeline.concurrency - self.running_operation_runs.count()

    def check_concurrency(self) -> bool:
        """ Check the pipeline concurrency.

        Checks the concurrency of the pipeline run
        to validate if we can start a new operation run.

        Returns:
            boolean: Whether to start a new operation run or not.
        """
        if not self.pipeline.concurrency:  # No concurrency set
            return True

        return self.n_operation_runs_to_start > 0
