from django.contrib.postgres.fields import JSONField
from django.db import models

from constants.jobs import JobLifeCycle
from db.models.utils import DiffModel, LastStatusMixin, StatusModel
from libs.resource_validation import validate_resource


class JobResources(models.Model):
    """A model that represents job resources."""
    cpu = JSONField(
        null=True,
        blank=True,
        validators=[validate_resource])
    memory = JSONField(
        null=True,
        blank=True,
        validators=[validate_resource])
    gpu = JSONField(
        null=True,
        blank=True,
        validators=[validate_resource])

    class Meta:
        app_label = 'db'
        verbose_name = 'job resources'
        verbose_name_plural = 'jobs resources'

    def __str__(self):
        def get_resource(resource, resource_name):
            if not resource:
                return ''
            return '{}: <{}-{}>'.format(resource_name,
                                        resource.get('requests'),
                                        resource.get('limits'))

        cpu = get_resource(self.cpu, 'CPU')
        memory = get_resource(self.memory, 'Memory')
        gpu = get_resource(self.gpu, 'GPU')
        resources = [cpu, memory, gpu]
        return ', '.join([r for r in resources if r])


class Job(DiffModel, LastStatusMixin):
    STATUSES = JobLifeCycle

    sequence = models.PositiveSmallIntegerField(
        editable=False,
        null=False,
        help_text='The sequence number of this job.', )

    class Meta:
        abstract = True

    @property
    def last_status(self):
        return self.job_status.status if self.job_status else None

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
        # We should not update constants anymore
        if JobLifeCycle.is_done(current_status):
            logger.info(
                'Received a new status `{}` for job `{}`. '
                'But the job is already done with status `{}`'.format(
                    status, self.unique_name, current_status))
            return False
        if status != current_status:
            # Add new status to the job
            status_model.objects.create(job=self,
                                        status=status,
                                        message=message,
                                        details=details)
            return True
        return False


class JobStatus(StatusModel):
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
