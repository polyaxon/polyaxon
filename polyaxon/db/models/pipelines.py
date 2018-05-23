import logging
import uuid

from celery.result import AsyncResult

from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.core.validators import validate_slug
from django.db import models
from django.dispatch import Signal

from libs.blacklist import validate_blacklist_name
from db.models.utils import DescribableModel, DiffModel, LastStatusMixin, StatusModel
from constants.pipelines import OperationStatuses, PipelineStatuses, TriggerPolicy
from polyaxon.celery_api import app as celery_app
from polyaxon.settings import Intervals

logger = logging.getLogger('db.pipelines')

status_change = Signal(providing_args=["instance", "status"])


class Schedule(DiffModel):
    """A model that represents the scheduling behaviour of an operation or a pipeline."""
    frequency = models.CharField(
        max_length=64,
        null=True,
        blank=True,
        help_text="Defines how often to run, "
                  "this timedelta object gets added to your latest operation instance's "
                  "execution_date to figure out the next schedule", )
    start_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="When this instance should run, "
                  "default is None which translate to now.")
    end_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="When this instance should stop running, "
                  "default is None which translate to open ended.")
    depends_on_past = models.BooleanField(
        default=False,
        help_text="when set to true, the instances will run "
                  "sequentially while relying on the previous instances' schedule to succeed.")

    class Meta:
        app_label = 'db'


class ExecutableModel(models.Model):
    """A model that represents an execution behaviour of an operation or a pipeline."""

    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        null=False)
    schedule = models.OneToOneField(
        'db.Schedule',
        null=True,
        blank=True,
        on_delete=models.SET_NULL)
    execute_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="When this instance should be executed. "
                  "default None which translate to now")
    timeout = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="specify how long this instance should be up "
                  "before timing out in seconds.")

    class Meta:
        abstract = True


class Pipeline(DiffModel, DescribableModel, ExecutableModel):
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
    name = models.CharField(
        max_length=256,
        validators=[validate_slug, validate_blacklist_name])
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='pipelines')
    project = models.ForeignKey(
        'db.Project',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='pipelines')
    concurrency = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        help_text="If set, it determines the number of operation instances "
                  "allowed to run concurrently.")

    class Meta:
        app_label = 'db'

    @property
    def dag(self):
        """Construct the DAG of this pipeline based on the its operations and their downstream."""
        from pipelines import dags

        operations = self.operations.all().prefetch_related('downstream_operations')

        def get_downstream(op):
            return op.downstream_operations.values_list('id', flat=True)

        return dags.get_dag(operations, get_downstream)


class Operation(DiffModel, DescribableModel, ExecutableModel):
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
    upstream_operations = models.ManyToManyField(
        "self",
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
    run_as_user = models.CharField(
        max_length=64,
        null=True,
        blank=True,
        help_text="unix username to impersonate while running the operation.")
    config = models.TextField(
        blank=True,
        null=True)
    celery_task = models.CharField(
        max_length=128,
        help_text="The celery task name to execute.")
    celery_queue = models.CharField(
        max_length=128,
        blank=True,
        null=True,
        help_text="The celery queue name to use for the executing this task. "
                  "If provided, it will override the queue provided in CELERY_TASK_ROUTES.")

    class Meta:
        app_label = 'db'

    def get_countdown(self, retries):
        """Calculate the countdown for a celery task retry."""
        retry_delay = self.retry_delay
        if self.retry_exponential_backoff:
            return min(
                max(2 ** retries, retry_delay),  # Exp. backoff
                self.max_retry_delay  # The countdown should be more the max allowed
            )
        return retry_delay

    def get_run_params(self):
        """Return the params to run the celery task."""
        params = {}
        if self.celery_queue:
            params['queue'] = self.celery_queue

        if self.timeout:
            params['soft_time_limit'] = self.timeout
            # We set also a hard time limit that will send sig 9
            # This hard time limit should not happened, as it will set inconsistent state
            params['time_limit'] = self.timeout + settings.CELERY_HARD_TIME_LIMIT_DELAY

        if self.execute_at:
            params['eta'] = self.execute_at

        return params


class PipelineRunStatus(StatusModel):
    """A model that represents a pipeline run status at certain time."""
    STATUSES = PipelineStatuses

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

    def __str__(self):
        return '{} <{}>'.format(self.pipeline_run, self.status)


class OperationRunStatus(StatusModel):
    """A model that represents an operation run status at certain time."""
    STATUSES = PipelineStatuses

    status = models.CharField(
        max_length=64,
        blank=True,
        null=True,
        default=STATUSES.CREATED,
        choices=STATUSES.CHOICES)
    operation_run = models.ForeignKey(
        'db.OperationRun',
        on_delete=models.CASCADE,
        related_name='statuses')

    class Meta:
        app_label = 'db'
        verbose_name_plural = 'Operation Run Statuses'
        ordering = ['created_at']

    def __str__(self):
        return '{} <{}>'.format(self.operation_run, self.status)


class RunModel(DiffModel, LastStatusMixin):
    """
    A model that represents an execution behaviour of instance/run of a operation or a pipeline.
    """
    STATUSES = None

    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        null=False)

    class Meta:
        abstract = True

    @property
    def last_status(self):
        return self.status.status if self.status else None

    @property
    def skipped(self):
        return self.STATUSES.skipped(self.last_status)

    @property
    def finished_at(self):
        status = self.statuses.filter(status__in=self.STATUSES.DONE_STATUS).first()
        if status:
            return status.created_at
        return None

    @property
    def started_at(self):
        status = self.statuses.filter(status=self.STATUSES.RUNNING).first()
        if status:
            return status.created_at
        return None

    def can_transition(self, status):
        """Update the status of the current instance.

        Returns:
            boolean: if the instance is updated.
        """
        if not self.STATUSES.can_transition(status_from=self.last_status, status_to=status):
            logger.info(
                '`%s` tried to transition from status `%s` to non permitted status `%s`',
                str(self), self.last_status, status)
            return False

        return True

    def on_scheduled(self, message=None):
        self.set_status(status=self.STATUSES.SCHEDULED, message=message)

    def on_run(self, message=None):
        self.set_status(status=self.STATUSES.RUNNING, message=message)

    def on_timeout(self, message=None):
        self.set_status(status=self.STATUSES.FAILED, message=message)

    def on_stop(self, message=None):
        self.set_status(status=self.STATUSES.STOPPED, message=message)

    def on_skip(self, message=None):
        self.set_status(status=self.STATUSES.SKIPPED, message=message)


class PipelineRun(RunModel):
    """A model that represents an execution behaviour/run of instance of a pipeline.

    Since this is an instance of known Pipeline,
    we can store the sorted topology of the dag,
    which should should not change during the execution time.
    """
    STATUSES = PipelineStatuses

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
    def dag(self):
        """Construct the DAG of this pipeline run
        based on the its operation runs and their downstream.
        """
        from pipelines import dags

        operation_runs = self.operation_runs.all().prefetch_related('downstream_runs')

        def get_downstream(op_run):
            return op_run.downstream_runs.values_list('id', flat=True)

        return dags.get_dag(operation_runs, get_downstream)

    def on_finished(self, message=None):
        self.set_status(status=self.STATUSES.FINISHED, message=message)

    def set_status(self, status, message=None, **kwargs):
        if not self.can_transition(status):
            return

        if PipelineStatuses.FINISHED != status:
            # If the status that we want to transition to is not a final state,
            # then no further checks are required
            PipelineRunStatus.objects.create(pipeline_run=self, status=status, message=message)
            return

        # If we reached a final state,
        # we mark the pipeline as FINISHED if all operation runs are finished
        all_op_runs_done = not bool([
            True for status in
            self.operation_runs.values_list('status__status', flat=True)
            if status not in OperationStatuses.DONE_STATUS
        ])
        if all_op_runs_done:
            PipelineRunStatus.objects.create(pipeline_run=self, status=status, message=message)

    @property
    def running_operation_runs(self):
        return self.operation_runs.filter(status__status__in=self.STATUSES.RUNNING_STATUS)

    @property
    def n_operation_runs_to_start(self):
        """We need to check if we are allowed to start any operations"""
        return self.pipeline.concurrency - self.running_operation_runs.count()

    def check_concurrency(self):
        """ Check the pipeline concurrency.

        Checks the concurrency of the pipeline run
        to validate if we can start a new operation run.

        Returns:
            boolean: Whether to start a new operation run or not.
        """
        if not self.pipeline.concurrency:  # No concurrency set
            return True

        return self.n_operation_runs_to_start > 0


class OperationRun(RunModel):
    """A model that represents an execution behaviour/run of instance of an operation."""
    STATUSES = OperationStatuses

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
    status = models.OneToOneField(
        'db.OperationRunStatus',
        related_name='+',
        blank=True,
        null=True,
        editable=True,
        on_delete=models.SET_NULL)
    celery_task_context = JSONField(
        blank=True,
        null=True,
        help_text='The kwargs required to execute the celery task.')
    celery_task_id = models.CharField(max_length=36, null=False, blank=True)

    class Meta:
        app_label = 'db'

    def set_status(self, status, message=None, **kwargs):
        if self.can_transition(status):
            OperationRunStatus.objects.create(operation_run=self, status=status, message=message)

    def check_concurrency(self):
        """Checks the concurrency of the operation run.

        Checks the concurrency of the operation run
        to validate if we can start a new operation run.

        Returns:
            boolean: Whether to start a new operation run or not.
        """
        if not self.operation.concurrency:  # No concurrency set
            return True

        ops_count = self.operation.runs.filter(
            status__status__in=self.STATUSES.RUNNING_STATUS).count()
        return ops_count < self.operation.concurrency

    def check_upstream_trigger(self):
        """Checks the upstream and the trigger rule."""
        if self.operation.trigger_policy == TriggerPolicy.ONE_DONE:
            return self.upstream_runs.filter(
                status__status__in=self.STATUSES.DONE_STATUS).exists()
        if self.operation.trigger_policy == TriggerPolicy.ONE_SUCCEEDED:
            return self.upstream_runs.filter(
                status__status=self.STATUSES.SUCCEEDED).exists()
        if self.operation.trigger_policy == TriggerPolicy.ONE_FAILED:
            return self.upstream_runs.filter(
                status__status=self.STATUSES.FAILED).exists()

        statuses = self.upstream_runs.values_list('status__status', flat=True)
        if self.operation.trigger_policy == TriggerPolicy.ALL_DONE:
            return not bool([True for status in statuses
                             if status not in self.STATUSES.DONE_STATUS])
        if self.operation.trigger_policy == TriggerPolicy.ALL_SUCCEEDED:
            return not bool([True for status in statuses
                             if status != self.STATUSES.SUCCEEDED])
        if self.operation.trigger_policy == TriggerPolicy.ALL_FAILED:
            return not bool([True for status in statuses
                             if status not in self.STATUSES.FAILED_STATUS])

    @property
    def is_upstream_done(self):
        statuses = self.upstream_runs.values_list('status__status', flat=True)
        return not bool([True for status in statuses
                         if status not in self.STATUSES.DONE_STATUS])

    def schedule_start(self):
        """Schedule the task: check first if the task can start:
            1. we check that the task is still in the CREATED state.
            2. we check that the upstream dependency is met.
            3. we check that pipeline can start a new task;
              i.e. we check the concurrency of the pipeline.
            4. we check that operation can start a new instance;
              i.e. we check the concurrency of the operation.

        -> If all checks pass we schedule the task start it.

        -> 1. If the operation is not in created status, nothing to do.
        -> 2. If the upstream dependency check is not met, two use cases need to be validated:
            * The upstream dependency is not met but could be met in the future,
              because some ops are still CREATED/SCHEDULED/RUNNING/...
              in this case nothing need to be done, every time an upstream operation finishes,
              it will notify all the downstream ops including this one.
            * The upstream dependency is not met and could not be met at all.
              In this case we need to mark the task with `UPSTREAM_FAILED`.
        -> 3. If the pipeline has reached it's concurrency limit,
           we just delay schedule based on the interval/time delay defined by the user.
           The pipeline scheduler will keep checking until the task can be scheduled or stopped.
        -> 4. If the operation has reached it's concurrency limit,
           Same as above we keep trying based on an interval defined by the user.

        Returns:
            boolean: Whether to try to schedule this operation run in the future or not.
        """
        if self.last_status != self.STATUSES.CREATED:
            return False

        upstream_trigger_check = self.check_upstream_trigger()
        if not upstream_trigger_check and self.is_upstream_done:
            # This task cannot be scheduled anymore
            self.on_upstream_failed()
            return False

        if not self.pipeline_run.check_concurrency():
            return True

        if not self.check_concurrency():
            return True

        self.on_scheduled()
        self.start()
        return False

    def start(self):
        """Start the celery task of this operation."""
        kwargs = self.celery_task_context
        # Update we the operation run id
        kwargs['operation_run_id'] = self.id  # pylint:disable=unsupported-assignment-operation

        async_result = celery_app.send_task(
            self.operation.celery_task,
            kwargs=kwargs,
            **self.operation.get_run_params())
        self.celery_task_id = async_result.id
        self.save()

    def stop(self, message=None):
        if self.is_running:
            task = AsyncResult(self.celery_task_id)
            task.revoke(terminate=True, signal='SIGKILL')
        self.on_stop(message=message)

    def skip(self, message=None):
        self.on_skip(message=message)

    def on_retry(self):
        self.set_status(status=self.STATUSES.RETRYING)

    def on_upstream_failed(self):
        self.set_status(status=self.STATUSES.UPSTREAM_FAILED)

    def on_failure(self, message=None):
        self.set_status(status=self.STATUSES.FAILED, message=message)
        self.save()

    def on_success(self, message=None):
        self.set_status(status=self.STATUSES.SUCCEEDED, message=message)
