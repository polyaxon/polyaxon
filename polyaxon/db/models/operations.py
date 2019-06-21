import logging
import uuid

from typing import Dict, Optional

from hestia.datetime_typing import AwareDT

from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.db.models import Q
from django.dispatch import Signal
from django.utils.functional import cached_property

from db.models.abstract.deleted import DeletedModel
from db.models.abstract.describable import DescribableModel
from db.models.abstract.diff import DiffModel
from db.models.abstract.executable import ExecutableModel
from db.models.abstract.nameable import NameableModel
from db.models.abstract.tag import TagModel
from db.models.abstract.unique_name import UniqueNameMixin
from db.models.statuses import LastStatusMixin
from db.models.unique_names import OPS_UNIQUE_NAME_FORMAT
from lifecycles.operations import OperationStatuses
from lifecycles.pipelines import TriggerPolicy
from polyaxon.settings import Intervals

_logger = logging.getLogger('db.operations')

status_change = Signal(providing_args=["instance", "status"])


class Operation(DiffModel,
                NameableModel,
                DescribableModel,
                TagModel,
                ExecutableModel,
                DeletedModel,
                UniqueNameMixin):
    """ Base class for all Operations.

    To derive this class, you are expected to override
    the constructor as well as the 'execute' method.

    Operations derived from this class should perform or trigger certain behaviour
    synchronously (wait for completion).

    Instantiating a class derived from this one results in the creation of a operation object,
    which ultimately could run independently or becomes a node in DAG objects.

    N.B.1: The `start_date` for the operation, determines
        the `execution_date` for the first operation instance. The best practice
        is to have the start_date rounded
        to your DAG's `schedule`. Daily jobs have their `start_date`
        some day at 00:00:00, hourly jobs have their start_date at 00:00
        of a specific hour. Note that Polyaxon simply looks at the latest
        `execution_date` and adds the `schedule_interval` to determine
        the next `execution_date`. It is also very important
        to note that different operations' dependencies
        need to line up in time. If operation A depends on operation B and their
        `start_date` are offset in a way that their execution_date don't line
        up, A's dependencies will never be met.

    Add for wait for downstream `wait_for_downstream` of upstream operations before running.
    """
    pipeline = models.ForeignKey(
        'db.Pipeline',
        on_delete=models.CASCADE,
        related_name='operations')
    schedule = models.OneToOneField(
        'db.Schedule',
        null=True,
        blank=True,
        on_delete=models.SET_NULL)
    upstream_operations = models.ManyToManyField(
        'self',
        blank=True,
        symmetrical=False,
        related_name='downstream_operations')
    trigger_policy = models.CharField(
        max_length=16,
        blank=True,
        null=True,
        default=TriggerPolicy.ALL_SUCCEEDED,
        choices=TriggerPolicy.CHOICES,
        help_text="defines the rule by which dependencies are applied, "
                  "default is `all_success`.")
    max_retries = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        help_text="the number of retries that should be performed before failing the operation.")
    k8s_retry = models.NullBooleanField(
        null=True,
        blank=True,
        default=True,
        help_text="Retry by setting the kubernetes retry field.")
    retry_delay = models.PositiveIntegerField(
        null=True,
        blank=True,
        default=Intervals.OPERATIONS_DEFAULT_RETRY_DELAY,
        help_text="The delay between retries.")
    retry_exponential_backoff = models.BooleanField(
        default=False,
        help_text="allow progressive longer waits between "
                  "retries by using exponential backoff algorithm on retry delay.")
    max_retry_delay = models.PositiveIntegerField(
        null=True,
        blank=True,
        default=Intervals.OPERATIONS_MAX_RETRY_DELAY,
        help_text="maximum delay interval between retries.")
    concurrency = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        help_text="When set, an operation will be able to limit the concurrent "
                  "runs across execution_dates")
    security_context = JSONField(
        max_length=64,
        null=True,
        blank=True,
        help_text="security context to impersonate while running the operation.")
    content = models.TextField(
        blank=True,
        null=True,
        help_text='The yaml content of the polyaxonfile/specification.')
    entity_type = models.CharField(
        max_length=24,
        blank=True,
        null=True)
    skip_on_upstream_skip = models.BooleanField(
        default=False,
        help_text="skip this operation if upstream operations are skipped.")
    queue = models.CharField(
        max_length=128,
        blank=True,
        null=True,
        help_text="The queue name to use for the executing this task. "
                  "If provided, it will override the queue provided in CELERY_TASK_ROUTES.")

    class Meta:
        app_label = 'db'
        unique_together = (('pipeline', 'name'),)
        indexes = [
            models.Index(fields=['name']),
        ]

    @cached_property
    def unique_name(self) -> str:
        return OPS_UNIQUE_NAME_FORMAT.format(
            pipeline_name=self.pipeline.unique_name,
            id=self.id)

    def get_countdown(self, retries) -> int:
        """Calculate the countdown for a celery task retry."""
        retry_delay = self.retry_delay
        if self.retry_exponential_backoff:
            return min(
                max(2 ** retries, retry_delay),  # Exp. backoff
                self.max_retry_delay  # The countdown should be more the max allowed
            )
        return retry_delay

    def get_run_params(self) -> Dict:
        """Return the params to run the celery task."""
        params = {}
        if self.queue:
            params['queue'] = self.queue

        if self.timeout:
            params['soft_time_limit'] = self.timeout
            # We set also a hard time limit that will send sig 9
            # This hard time limit should not happened, as it will set inconsistent state
            params['time_limit'] = self.timeout + settings.CELERY_HARD_TIME_LIMIT_DELAY

        if self.execute_at:
            params['eta'] = self.execute_at

        return params


class OperationRun(DiffModel, DeletedModel, LastStatusMixin):
    """A model that represents an execution behaviour/run of instance of an operation."""
    STATUSES = OperationStatuses

    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        null=False)
    operation = models.ForeignKey(
        'db.Operation',
        on_delete=models.CASCADE,
        related_name='runs')
    pipeline_run = models.ForeignKey(
        'db.PipelineRun',
        on_delete=models.CASCADE,
        related_name='operation_runs')
    upstream_runs = models.ManyToManyField(
        'self',
        blank=True,
        symmetrical=False,
        related_name='downstream_runs')
    entity_content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='+')
    entity_object_id = models.PositiveIntegerField(
        blank=True,
        null=True,
    )
    entity = GenericForeignKey('entity_content_type', 'entity_object_id')
    status = models.CharField(
        max_length=64,
        blank=True,
        null=True)
    context = JSONField(
        blank=True,
        null=True,
        help_text='The kwargs required to execute the celery task.')

    class Meta:
        app_label = 'db'

    @property
    def started_at(self):
        return self.entity.started_at if self.entity else None

    @property
    def finished_at(self):
        return self.entity.finished_at if self.entity else None

    @property
    def last_status(self):
        return self.status

    def last_status_before(self, status_date: AwareDT = None) -> Optional[str]:
        return self.entity.last_status_before(status_date=status_date) if self.entity else None

    def set_status(self,
                   status: str,
                   created_at: AwareDT = None,
                   message: str = None,
                   traceback: Dict = None,
                   **kwargs) -> None:
        if self.entity:
            self.entity.set_status(status=status,
                                   created_at=created_at,
                                   message=message,
                                   traceback=traceback,
                                   **kwargs)

    def check_concurrency(self) -> bool:
        """Checks the concurrency of the operation run.

        Checks the concurrency of the operation run
        to validate if we can start a new operation run.

        Returns:
            boolean: Whether to start a new operation run or not.
        """
        if not self.operation.concurrency:  # No concurrency set
            return True

        ops_count = self.operation.runs.exclude(Q(status__in=OperationStatuses.DONE_STATUS) |
                                                Q(status__isnull=True)).count()
        return ops_count < self.operation.concurrency

    def check_upstream_trigger(self) -> bool:
        """Checks the upstream and the trigger rule."""
        if self.operation.trigger_policy == TriggerPolicy.ONE_DONE:
            return self.upstream_runs.filter(status__in=OperationStatuses.DONE_STATUS).exists()
        if self.operation.trigger_policy == TriggerPolicy.ONE_SUCCEEDED:
            return self.upstream_runs.filter(status=OperationStatuses.SUCCEEDED).exists()
        if self.operation.trigger_policy == TriggerPolicy.ONE_FAILED:
            return self.upstream_runs.filter(status=OperationStatuses.FAILED).exists()

        statuses = self.upstream_runs.values_list('status', flat=True)
        if self.operation.trigger_policy == TriggerPolicy.ALL_DONE:
            return not bool([True for status in statuses
                             if status not in OperationStatuses.DONE_STATUS])
        if self.operation.trigger_policy == TriggerPolicy.ALL_SUCCEEDED:
            return not bool([True for status in statuses
                             if status != OperationStatuses.SUCCEEDED])
        if self.operation.trigger_policy == TriggerPolicy.ALL_FAILED:
            return not bool([True for status in statuses
                             if status not in OperationStatuses.FAILED_STATUS])

    @property
    def is_upstream_done(self) -> bool:
        statuses = self.upstream_runs.values_list('status', flat=True)
        return not bool([True for status in statuses
                         if status not in OperationStatuses.DONE_STATUS])

    def on_retry(self) -> None:
        if self.entity:
            self.entity.set_status(status=OperationStatuses.RETRYING)
        else:
            self.status = OperationStatuses.RETRYING
            self.save(update_fields=['status'])

    def on_upstream_failed(self) -> None:
        if self.entity:
            self.entity.set_status(status=OperationStatuses.UPSTREAM_FAILED)
        else:
            self.status = OperationStatuses.UPSTREAM_FAILED
            self.save(update_fields=['status'])

    def on_failure(self, message: str = None) -> None:
        if self.entity:
            self.entity.set_status(status=OperationStatuses.FAILED, message=message)
        else:
            self.status = OperationStatuses.FAILED
            self.save(update_fields=['status'])

    def on_success(self, message: str = None) -> None:
        if self.entity:
            self.entity.set_status(status=OperationStatuses.SUCCEEDED, message=message)
        else:
            self.status = OperationStatuses.SUCCEEDED
            self.save(update_fields=['status'])
