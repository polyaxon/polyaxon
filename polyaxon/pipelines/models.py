from django.conf import settings
from django.db import models

from libs.models import DiffModel, DescribableModel
from pipelines.constants import OperationStatus, TriggerRule


class Schedule(DiffModel):
    """A model that represents the scheduling behaviour of a operation or a pipeline."""
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
    """A model that represents an execution behaviour of a operation or a pipeline."""
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
    started_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="When the started.")
    finished_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="When the finished.")
    status = models.CharField(
        max_length=16,
        blank=True,
        null=True,
        default=OperationStatus.CREATED,
        choices=OperationStatus.CHOICES)

    class Meta:
        abstract = True

    def on_timeout(self):
        pass

    def on_failure(self):
        pass

    def on_success(self):
        pass


class UpstreamModel(models.Model):
    """A model that represents the dependency behaviour of a operation or a pipeline."""
    DOWNSTREAM_RELATED_NAME = ''

    upstream_operations = models.ManyToManyField(
        "pipelines.Operation",
        blank=True,
        null=True,
        related_name=DOWNSTREAM_RELATED_NAME)
    upstream_pipelines = models.ManyToManyField(
        "pipelines.Pipeline",
        blank=True,
        null=True,
        related_name=DOWNSTREAM_RELATED_NAME)
    trigger_rule = models.CharField(
        max_length=16,
        blank=True,
        null=True,
        default=TriggerRule.ALL_SUCCESS,
        choices=TriggerRule.CHOICES,
        help_text="defines the rule by which dependencies are applied, "
                  "default is `all_success`.")

    class Meta:
        abstract = True

    def can_start(self):
        """Checks the upstream and the trigger rule."""
        if self.trigger_rule == TriggerRule.ONE_DONE:
            operation_check = self.upstream_operations.filter(
                status__in=OperationStatus.DONE_STATUS).exists()
            if operation_check:
                return True
            return self.upstream_pipelines.filter(
                status__in=OperationStatus.DONE_STATUS).exists()
        if self.trigger_rule == TriggerRule.ONE_SUCCESS:
            operation_check = self.upstream_operations.filter(
                status=OperationStatus.SUCCESS).exists()
            if operation_check:
                return True
            return self.upstream_pipelines.filter(status=OperationStatus.SUCCESS).exists()
        if self.trigger_rule == TriggerRule.ONE_FAILED:
            operation_check = self.upstream_operations.filter(
                status=OperationStatus.FAILED).exists()
            if operation_check:
                return True
            return self.upstream_pipelines.filter(status=OperationStatus.FAILED).exists()
        if self.trigger_rule == TriggerRule.ALL_DONE:
            operation_check = self.upstream_operations.exclude(
                status__in=OperationStatus.DONE_STATUS).exists()
            if not operation_check:
                return False
            return self.upstream_pipelines.exclude(
                status__in=OperationStatus.DONE_STATUS).exists()
        if self.trigger_rule == TriggerRule.ALL_SUCCESS:
            operation_check = self.upstream_operations.exclude(
                status=OperationStatus.SUCCESS).exists()
            if not operation_check:
                return False
            return self.upstream_pipelines.exclude(status=OperationStatus.SUCCESS).exists()
        if self.trigger_rule == TriggerRule.ALL_FAILED:
            operation_check = self.upstream_operations.exclude(
                status=OperationStatus.FAILED).exists()
            if not operation_check:
                return False
            return self.upstream_pipelines.exclude(status=OperationStatus.FAILED).exists()

    def notify_downstream(self):
        """Notify downstream that this instance is done, and that its dependency can start."""
        for pipeline in self.downstream_operations.filter(status=OperationStatus.CREATED):
            pipeline.check_and_start()
        for pipeline in self.downstream_pipelines.filter(status=OperationStatus.CREATED):
            pipeline.check_and_start()


class Pipeline(DiffModel, DescribableModel, UpstreamModel, ExecutableModel):
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
    DOWNSTREAM_RELATED_NAME = 'downstream_pipelines'
    EXECUTABLE_RELATED_NAME = 'pipelines'

    concurrency = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        help_text="the number of operation instances allowed to run concurrently")


class Operation(DiffModel, DescribableModel, UpstreamModel, ExecutableModel):
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
    DOWNSTREAM_RELATED_NAME = 'downstream_operations'
    EXECUTABLE_RELATED_NAME = 'operations'

    pipeline = models.ForeignKey(
        Pipeline,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='operations')
    n_retries = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        help_text="the number of retries that should be performed before failing the operation.")
    retry_delay = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="The delay between retries.")
    retry_exponential_backoff = models.BooleanField(
        default=False,
        help_text="allow progressive longer waits between "
                  "retries by using exponential backoff algorithm on retry delay.")
    max_retry_delay = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="maximum delay interval between retries.")
    concurrency = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        help_text="When set, a operation will be able to limit the concurrent "
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

    @property
    def independent(self):
        return self.pipeline is None

    def on_retry(self):
        pass
