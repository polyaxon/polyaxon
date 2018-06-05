import uuid

from django.contrib.postgres.fields import JSONField
from django.db import models

from constants.jobs import JobLifeCycle
from db.models.utils import DiffModel, LastStatusMixin, StatusModel


class AbstractJob(DiffModel, LastStatusMixin):
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

    def _set_status(self, status_model, logger, status, message=None, details=None):
        current_status = self.last_status
        if self.is_done:
            # We should not update statuses anymore
            logger.info(
                'Received a new status `{}` for job `{}`. '
                'But the job is already done with status `{}`'.format(
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
