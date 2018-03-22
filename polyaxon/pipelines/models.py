from django.conf import settings
from django.db import models

from libs.models import DiffModel, DescribableModel
from pipelines.constants import TaskStatus, TriggerRule


class Schedule(DiffModel):
    """A model that represents the scheduling behaviour of a task or a pipeline."""
    frequency = models.CharField(
        max_length=64,
        null=True,
        blank=True,
        help_text="Defines how often a pipeline/task runs, "
                  "this timedelta object gets added to your latest task instance's "
                  "execution_date to figure out the next schedule", )
    start_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="When the pipeline/task should run, "
                  "default is None which translate to now.")
    end_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="When the pipeline/task should stop running, "
                  "default is None which translate to open ended.")


class CallbackMixin(object):
    def on_timeout(self):
        pass

    def on_failure(self):
        pass

    def on_success(self):
        pass


class UpstreamModel(models.Model):
    """A model that represents the dependency behaviour of a task or a pipeline."""
    DOWNSTREAM_RELATED_NAME = ''

    upstream_tasks = models.ManyToManyField(
        "pipelines.Task",
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
        help_text="defines the rule by which dependencies are applied "
                  "default is `all_success`. "
                  "Options can be set as string or for the task to get triggered. "
                  "Options are: "
                  "`{ all_success | all_failed | all_done | one_success | one_failed | any}`")

    class Meta:
        abstract = True

    def should_start(self):
        """Checks the upstream and the trigger rule."""
        if self.trigger_rule == TriggerRule.ANY:
            return True


class Pipeline(DiffModel, DescribableModel, UpstreamModel, CallbackMixin):
    """A model that represents a pipeline (DAG - directed acyclic graph).

    A Pipeline is a collection / namespace of tasks with directional dependencies.
    A Pipeline can optionally have
     * a schedule (e.g. daily, hourly, ...)
     * a start end an end date

    Every task has dependencies, and can only run when all the dependencies are met.

    Certain tasks can depend on their own past, i.e that they can't run
    until their previous schedule (and upstream tasks) are completed.

    A pipeline can also have dependencies/upstream dags/tasks.
    """
    DOWNSTREAM_RELATED_NAME = 'downstream_pipelines'

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='pipelines')
    schedule = models.OneToOneField(
        Schedule,
        null=True,
        blank=True,
        on_delete=models.SET_NULL)
    execute_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="When the task should be executed. "
                  "default None which translate to now")
    concurrency = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        help_text="the number of task instances allowed to run concurrently")
    timeout = models.DurationField(
        null=True,
        blank=True,
        help_text="specify how long a pipeline should be up before timing out in seconds.")


class Task(DiffModel, DescribableModel, UpstreamModel, CallbackMixin):
    """ Base class for all Tasks.

    To derive this class, you are expected to override
    the constructor as well as the 'execute' method.

    Tasks derived from this class should perform or trigger certain behaviour
    synchronously (wait for completion).

    Instantiating a class derived from this one results in the creation of a task object,
    which ultimately could run independently or becomes a node in DAG objects.

    N.B.1: The `start_date` for the task, determines
        the `execution_date` for the first task instance. The best practice
        is to have the start_date rounded
        to your DAG's `schedule`. Daily jobs have their `start_date`
        some day at 00:00:00, hourly jobs have their start_date at 00:00
        of a specific hour. Note that Polyaxon simply looks at the latest
        `execution_date` and adds the `schedule_interval` to determine
        the next `execution_date`. It is also very important
        to note that different tasks' dependencies
        need to line up in time. If task A depends on task B and their
        `start_date` are offset in a way that their execution_date don't line
        up, A's dependencies will never be met.

    Add for wait for downstream `wait_for_downstream` of upstream tasks before running.
    """
    DOWNSTREAM_RELATED_NAME = 'downstream_tasks'

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='tasks')
    pipeline = models.ForeignKey(
        Pipeline,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='tasks')
    schedule = models.OneToOneField(
        Schedule,
        null=True,
        blank=True,
        on_delete=models.SET_NULL)
    execute_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="When the task should be executed. "
                  "default None which translate to now")
    n_retries = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        help_text="the number of retries that should be performed before failing the task.")
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
    start_date = models.DateTimeField(
        null=True,
        blank=True,
        help_text="start date of the task, "
                  "default is None which translate to now.")
    end_date = models.DateTimeField(
        null=True,
        blank=True,
        help_text="When the task should stop running, "
                  "default is None which translate to open ended.")
    depends_on_past = models.BooleanField(
        default=False,
        help_text="when set to true, task instances will run "
                  "sequentially while relying on the previous task's schedule to succeed. "
                  "The task instance for the start_date is allowed to run.")
    timeout = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="specify how long a task should be up before timing out in seconds.")
    concurrency = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        help_text="When set, a task will be able to limit the concurrent "
                  "runs across execution_dates")
    run_as_user = models.CharField(
        max_length=64,
        null=True,
        blank=True,
        help_text="unix username to impersonate while running the task.")
    resources = models.OneToOneField(
        'jobs.JobResources',
        on_delete=models.SET_NULL,
        null=True,
        blank=True)

    @property
    def independent(self):
        return self.pipeline is None


class TaskRun(models.Model):
    """ A model that represents a run of Task."""
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name='runs')
    pipeline = models.ForeignKey(
        Pipeline,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='tasks')
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
        default=TaskStatus.STARTED,
        choices=TaskStatus.CHOICES)
