import logging
import uuid

from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.functional import cached_property

from constants.jobs import JobLifeCycle
from db.models.utils import DiffModel, LastStatusMixin, StatusModel

_logger = logging.getLogger('polyaxon.db.jobs')


class AbstractJob(DiffModel, LastStatusMixin):
    """An abstract base class for job, used both by experiment jobs and other jobs."""
    STATUSES = JobLifeCycle

    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        null=False)
    sequence = models.PositiveSmallIntegerField(
        editable=False,
        null=False,
        help_text='The sequence number of this job.', )
    definition = JSONField(help_text='The specific values/manifest for this job.', default={})

    class Meta:
        abstract = True

    @property
    def last_status(self):
        return self.status.status if self.status else None

    @property
    def started_at(self):
        status = self.statuses.filter(status=JobLifeCycle.BUILDING).first()
        if not status:
            status = self.statuses.filter(status=JobLifeCycle.RUNNING).first()
        if status:
            return status.created_at
        return None

    @property
    def finished_at(self):
        status = self.statuses.filter(status__in=JobLifeCycle.DONE_STATUS).last()
        if status:
            return status.created_at
        return None

    def _set_status(self, status_model, status, message=None, details=None):
        current_status = self.last_status
        if self.is_done:
            # We should not update statuses anymore
            _logger.debug(
                'Received a new status `%s` for job `%s`. '
                'But the job is already done with status `%s`', (
                    status, self.unique_name, current_status))
            return False
        if JobLifeCycle.can_transition(status_from=current_status, status_to=status):
            # Add new status to the job
            status_model.objects.create(job=self,
                                        status=status,
                                        message=message,
                                        details=details)
            return True
        return False


class JobMixin(object):

    @cached_property
    def unique_name(self):
        return self.__str__()

    @cached_property
    def image(self):
        return self.specification.build.image

    @cached_property
    def resources(self):
        return self.specification.resources

    @cached_property
    def node_selectors(self):
        return self.specification.node_selectors

    @cached_property
    def build_steps(self):
        return self.specification.build.build_steps

    @cached_property
    def env_vars(self):
        return self.specification.build.env_vars


class AbstractJobStatus(StatusModel):
    """A model that represents job status at certain time."""
    STATUSES = JobLifeCycle

    status = models.CharField(
        max_length=64,
        blank=True,
        null=True,
        default=STATUSES.CREATED,
        choices=STATUSES.CHOICES)
    details = JSONField(null=True, blank=True, default={})

    def __str__(self):
        return '{} <{}>'.format(self.job.unique_name, self.status)

    class Meta:
        verbose_name_plural = 'Job Statuses'
        ordering = ['created_at']
        abstract = True
