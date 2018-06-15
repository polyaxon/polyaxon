from django.db import models

from db.models.abstract_jobs import AbstractJob, AbstractJobStatus
from polyaxon_schemas.utils import TaskType


class ExperimentJob(AbstractJob):
    """A model that represents job related to an experiment"""
    experiment = models.ForeignKey(
        'db.Experiment',
        on_delete=models.CASCADE,
        related_name='jobs')
    role = models.CharField(max_length=64, default=TaskType.MASTER)
    resources = models.OneToOneField(
        'db.JobResources',
        related_name='+',
        blank=True,
        null=True,
        editable=True,
        on_delete=models.SET_NULL)
    status = models.OneToOneField(
        'db.ExperimentJobStatus',
        related_name='+',
        blank=True,
        null=True,
        editable=True,
        on_delete=models.SET_NULL)

    class Meta:
        app_label = 'db'
        unique_together = (('experiment', 'sequence'),)

    def save(self, *args, **kwargs):  # pylint:disable=arguments-differ
        filter_query = ExperimentJob.sequence_objects.filter(experiment=self.experiment)
        self._set_sequence(filter_query=filter_query)
        super(ExperimentJob, self).save(*args, **kwargs)

    def __str__(self):
        return self.unique_name

    @property
    def unique_name(self):
        return '{}.{}.{}'.format(self.experiment.unique_name, self.sequence, self.role)

    def set_status(self, status, message=None, details=None):  # pylint:disable=arguments-differ
        return self._set_status(status_model=ExperimentJobStatus,
                                status=status,
                                message=message,
                                details=details)


class ExperimentJobStatus(AbstractJobStatus):
    """A model that represents job status at certain time."""
    job = models.ForeignKey(
        'db.ExperimentJob',
        on_delete=models.CASCADE,
        related_name='statuses')

    class Meta(AbstractJobStatus.Meta):
        app_label = 'db'
        verbose_name_plural = 'Experiment Job Statuses'
