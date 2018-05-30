import logging
import uuid

from django.contrib.postgres.fields import JSONField
from django.db import models

from db.models.jobs import Job, JobStatus
from polyaxon_schemas.utils import TaskType

logger = logging.getLogger('db.experiments')


class ExperimentJob(Job):
    """A model that represents job related to an experiment"""
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        null=False)
    experiment = models.ForeignKey(
        'db.Experiment',
        on_delete=models.CASCADE,
        related_name='jobs')
    definition = JSONField(help_text='The specific values for this job.')
    role = models.CharField(max_length=64, default=TaskType.MASTER)
    sequence = models.PositiveSmallIntegerField(
        editable=False,
        null=False,
        help_text='The sequence number of this job within the experiment.', )
    resources = models.OneToOneField(
        'db.JobResources',
        related_name='+',
        blank=True,
        null=True,
        editable=True,
        on_delete=models.SET_NULL)
    job_status = models.OneToOneField(
        'db.ExperimentJobStatus',
        related_name='+',
        blank=True,
        null=True,
        editable=True,
        on_delete=models.SET_NULL)

    class Meta:
        app_label = 'db'
        ordering = ['sequence']
        unique_together = (('experiment', 'sequence'),)

    def __str__(self):
        return self.unique_name

    @property
    def unique_name(self):
        return '{}.{}.{}'.format(self.experiment.unique_name, self.sequence, self.role)

    def save(self, *args, **kwargs):  # pylint:disable=arguments-differ
        if self.pk is None:
            last = ExperimentJob.objects.filter(experiment=self.experiment).last()
            self.sequence = 1
            if last:
                self.sequence = last.sequence + 1

        super(ExperimentJob, self).save(*args, **kwargs)

    def set_status(self, status, message=None, details=None):  # pylint:disable=arguments-differ
        return self._set_status(status_model=ExperimentJobStatus,
                                logger=logger,
                                status=status,
                                message=message,
                                details=details)


class ExperimentJobStatus(JobStatus):
    """A model that represents job status at certain time."""
    job = models.ForeignKey(
        'db.ExperimentJob',
        on_delete=models.CASCADE,
        related_name='statuses')

    class Meta(JobStatus.Meta):
        app_label = 'db'
        verbose_name_plural = 'Experiment Job Statuses'
