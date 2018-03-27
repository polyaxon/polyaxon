import logging

from celery.result import AsyncResult

from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.dispatch import Signal
from django.utils import timezone

from pipelines import dags
from polyaxon.celery_api import app as celery_app
from polyaxon.settings import Intervals

from libs.models import DiffModel, DescribableModel
from pipelines.constants import OperationStatuses, PipelineStatuses, TriggerRule

logger = logging.getLogger('polyaxon.pipelines')


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


class ExecutableModel(models.Model):
    """A model that represents an execution behaviour of an operation or a pipeline."""
    EXECUTABLE_RELATED_NAME = ''

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name=EXECUTABLE_RELATED_NAME)
    schedule = models.OneToOneField(
        Schedule,
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
    EXECUTABLE_RELATED_NAME = 'pipelines'

    concurrency = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        help_text="If set, it determines the number of operation instances "
                  "allowed to run concurrently.")

    @property
    def dag(self):
        """Construct the DAG of this pipeline based on the its operations and their downstream."""
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
    EXECUTABLE_RELATED_NAME = 'operations'

    pipeline = models.ForeignKey(
        Pipeline,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='operations')
    upstream_operations = models.ManyToManyField(
        "self",
        blank=True,
        null=True,
        related_name='downstream_operations')
    trigger_rule = models.CharField(
        max_length=16,
        blank=True,
        null=True,
        default=TriggerRule.ALL_SUCCESS,
        choices=TriggerRule.CHOICES,
        help_text="defines the rule by which dependencies are applied, "
                  "default is `all_success`.")
    max_retries = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        help_text="the number of retries that should be performed before failing the operation.")
    retry_delay = models.PositiveIntegerField(
        null=True,
        blank=True,
        default=Intervals.DEFAULT_RETRY_DELAY,
        help_text="The delay between retries.")
    retry_exponential_backoff = models.BooleanField(
        default=False,
        help_text="allow progressive longer waits between "
                  "retries by using exponential backoff algorithm on retry delay.")
    max_retry_delay = models.PositiveIntegerField(
        null=True,
        blank=True,
        default=Intervals.MAX_RETRY_DELAY,
        help_text="maximum delay interval between retries.")
    n_retries = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        help_text="the number of retries that performed so far by the operations.")
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
    resources = models.OneToOneField(
        'jobs.JobResources',
        on_delete=models.SET_NULL,
        null=True,
        blank=True)
    celery_task = models.CharField(
        max_length=128,
        help_text="The celery task name to execute.")
    celery_queue = models.CharField(
        max_length=128,
        blank=True,
        null=True,
        help_text="The celery queue name to use for the executing this task. "
                  "If provided, it will override the queue provided in CELERY_TASK_ROUTES.")

    @property
    def independent(self):
        return self.pipeline is None

    def get_countdown(self, retries):
        """Calculate the countdown for a celery task retry."""
        retry_delay = self.retry_delay
        if self.retry_exponential_backoff:
            return min(
                max(2 ** retries, retry_delay),  # Exp. backoff
                self.max_retry_delay  # The countdown should be more the max allowed
            )
        else:
            return retry_delay

    def get_run_kwargs(self):
        """Return the kwargs to run the celery task."""
        kwargs = {}
        if self.celery_queue:
            kwargs['queue'] = self.celery_queue

        if self.timeout:
            kwargs['soft_time_limit'] = self.timeout
            # We set also a hard time limit that will send sig 9
            # This hard time limit should not happened, as it will set inconsistent state
            kwargs['time_limit'] = self.timeout + settings.CELERY_HARD_TIME_LIMIT_DELAY

        if self.execute_at:
            kwargs['eta'] = self.execute_at

        return kwargs


class RunModel(DiffModel):
    """
    A model that represents an execution behaviour of instance/run of a operation or a pipeline.
    """
    STATUSES = None

    started_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="When the instance started.")
    finished_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="When the instance finished.")
    status = models.CharField(
        max_length=16,
        blank=True,
        null=True,
        default=STATUSES.CREATED,
        choices=STATUSES.CHOICES)

    class Meta:
        abstract = True

    def update_status(self, status):
        """Update the status of the current instance.

        Returns:
            boolean: if the instance is updated.
        """
        if self.status == status:
            return False

        if not self.STATUSES.can_transition(status_from=self.status, status_to=status):
            logger.warning(
                '`{}` tried to transition from status `{}` to non permitted status `{}`'.format(
                    str(self), self.status, status))
            return False

        self.status = status
        status_change.send(sender=self.__class__, instance=self, status=status)
        return True

    def notify_status_changed(self):
        pass

    def on_scheduled(self):
        self.update_status(status=self.STATUSES.SCHEDULED)
        self.save()

    def on_run(self):
        self.update_status(status=self.STATUSES.RUNNING)
        self.started_at = timezone.now()
        self.save()

    def on_timeout(self):
        self.update_status(status=self.STATUSES.FAILED)
        self.finished_at = timezone.now()
        self.save()

    def on_failure(self):
        self.update_status(status=self.STATUSES.FAILED)
        self.finished_at = timezone.now()
        self.save()

    def on_success(self):
        self.update_status(status=self.STATUSES.SUCCESS)
        self.finished_at = timezone.now()
        self.save()

    def on_stop(self):
        self.update_status(status=self.STATUSES.STOPPED)
        self.finished_at = timezone.now()
        self.save()

    def on_skip(self):
        self.update_status(status=self.STATUSES.SKIPPED)
        self.finished_at = timezone.now()
        self.save()


class PipelineRun(RunModel):
    """A model that represents an execution behaviour/run of instance of a pipeline.

    Since this is an instance of known Pipeline,
    we can store the sorted topology of the dag,
    which should should not change during the execution time.
    """
    STATUSES = PipelineStatuses

    pipeline = models.ForeignKey(
        Pipeline,
        on_delete=models.CASCADE,
        related_name='runs')

    @property
    def dag(self):
        """Construct the DAG of this pipeline run
        based on the its operation runs and their downstream.
        """
        operation_runs = self.operation_runs.all().prefetch_related('downstream_operations')

        def get_downstream(op_run):
            return op_run.operation_runs.values_list('id', flat=True)

        return dags.get_dag(operation_runs, get_downstream)

    def check_concurrency(self):
        """Checks the concurrency of the pipeline run to validate if we can start a new operation run.

        Returns:
            boolean: Whether to start a new operation run or not.
        """
        if not self.pipeline.concurrency:  # No concurrency set
            return True

        ops_count = self.operation_runs.filter(status__in=self.STATUSES.RUNNING_STATUS).count()
        return ops_count < self.pipeline.concurrency

    def notify_status_changed(self):
        """Notification logic for pipeline runs:

            * notify operations with status change.
            * other notification if configured on the pipeline.
        """
        pass


class OperationRun(RunModel):
    """A model that represents an execution behaviour/run of instance of an operation."""
    STATUSES = OperationStatuses

    operation = models.ForeignKey(
        Operation,
        on_delete=models.CASCADE,
        related_name='runs')
    pipeline_run = models.ForeignKey(
        PipelineRun,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='operation_runs')
    upstream_runs = models.ManyToManyField(
        'self',
        blank=True,
        null=True,
        related_name='downstream_runs')
    retried_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="When the instance last retried.")
    celery_task_context = JSONField(
        blank=True,
        null=True,
        help_text='The kwargs required to execute the celery task.')
    celery_task_id = models.UUIDField(null=False, blank=True)

    def check_concurrency(self):
        """Checks the concurrency of the operation run to validate if we can start a new operation run.

        Returns:
            boolean: Whether to start a new operation run or not.
        """
        if not self.operation.concurrency:  # No concurrency set
            return True

        ops_count = self.operation.runs.filter(status__in=self.STATUSES.RUNNING_STATUS).count()
        return ops_count < self.operation.concurrency

    def check_upstream_trigger(self):
        """Checks the upstream and the trigger rule."""
        if self.operation.trigger_rule == TriggerRule.ONE_DONE:
            return self.upstream_runs.filter(
                status__in=self.STATUSES.DONE_STATUS).exists()
        if self.operation.trigger_rule == TriggerRule.ONE_SUCCESS:
            return self.upstream_runs.filter(
                status=self.STATUSES.SUCCESS).exists()
        if self.operation.trigger_rule == TriggerRule.ONE_FAILED:
            return self.upstream_runs.filter(
                status=self.STATUSES.FAILED).exists()
        if self.operation.trigger_rule == TriggerRule.ALL_DONE:
            return self.upstream_runs.exclude(
                status__in=self.STATUSES.DONE_STATUS).exists()
        if self.operation.trigger_rule == TriggerRule.ALL_SUCCESS:
            return self.upstream_runs.exclude(
                status=self.STATUSES.SUCCESS).exists()
        if self.operation.trigger_rule == TriggerRule.ALL_FAILED:
            return self.upstream_runs.exclude(
                status=self.STATUSES.FAILED).exists()

    @property
    def is_upstream_done(self):
        upstream_count = self.upstream_runs.count()
        upstream_done_count = self.upstream_runs.exclude(
            status__in=self.STATUSES.DONE_STATUS).count()
        return upstream_count == upstream_done_count

    def notify_pipeline(self):
        # If the operation run is updated, we need to notify the pipeline run
        if self.status in PipelineStatuses.VALUES:
            # TODO This is not correct, the pipeline must check for all tasks to decide on the status
            self.pipeline_run.update_status(status=self.status)
        # One case that we also need to handle
        if self.status == self.STATUSES.UPSTREAM_FAILED:
            # TODO: may be we need to call on_failure, to notify the rest of the operations to stop.
            self.pipeline_run.update_status(status=PipelineStatuses.FAILED)

    def notify_downstream(self):
        """Notify downstream that this instance is done, and that its dependency can start."""
        for op in self.downstream_runs.filter(status=self.STATUSES.CREATED):
            op.schedule_start()

    def notify_status_changed(self):
        """Notification logic for operation runs:

            * notify downstream with status change
            * notify pipeline with status change
            * other notification if configured on the pipeline
        """
        self.notify_pipeline()
        self.notify_downstream()

    def schedule_start(self):
        """Schedule the task: check first if the task can start:
            1. we check that the task did not reach a end status;
              e.g. was `STOPPED` or marked as `SKIPPED`.
            2. we check that the upstream dependency is met.
            3. we check that pipeline can start a new task;
              i.e. we check the concurrency of the pipeline.
            4. we check that operation can start a new instance;
              i.e. we check the concurrency of the operation.

        -> If all checks pass we schedule the task start it.

        -> 1. If the operation is in end status: nothing should be done.
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
        if self.status in self.STATUSES.DONE_STATUS:
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
        async_result = celery_app.send_task(
            self.operation.celery_task,
            kwargs=self.celery_task_context,
            **self.operation.get_run_kwargs())
        self.celery_task_id = async_result.id
        self.save()

    def stop(self):
        task = AsyncResult(self.celery_task_id)
        task.revoke(terminate=True, signal='SIGKILL')
        self.on_stop()

    def skip(self):
        self.on_skip()

    def on_retry(self):
        self.update_status(status=self.STATUSES.RETRYING)
        self.retried_at = timezone.now()
        self.save()

    def on_upstream_failed(self):
        self.update_status(status=self.STATUSES.UPSTREAM_FAILED)
        self.finished_at = timezone.now()
        self.save()
