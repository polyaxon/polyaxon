import logging

from django.db import models
from django.utils.functional import cached_property

from db.models.abstract_jobs import AbstractJobStatus
from db.models.plugins import PluginJobBase

_logger = logging.getLogger('db.tensorboards')


class TensorboardJob(PluginJobBase):
    """A model that represents the configuration for tensorboard job."""
    project = models.ForeignKey(
        'db.Project',
        on_delete=models.CASCADE,
        related_name='tensorboard_jobs')
    experiment_group = models.ForeignKey(
        'db.ExperimentGroup',
        on_delete=models.CASCADE,
        related_name='tensorboard_jobs',
        null=True,
        blank=True)
    experiment = models.ForeignKey(
        'db.Experiment',
        on_delete=models.CASCADE,
        related_name='tensorboard_jobs',
        null=True,
        blank=True)
    status = models.OneToOneField(
        'db.TensorboardJobStatus',
        related_name='+',
        blank=True,
        null=True,
        editable=True,
        on_delete=models.SET_NULL)

    class Meta:
        app_label = 'db'

    def __str__(self):
        return self.unique_name

    def save(self, *args, **kwargs):  # pylint:disable=arguments-differ
        if self.pk is None:
            last = TensorboardJob.objects.filter(project=self.project).last()
            self.sequence = 1
            if last:
                self.sequence = last.sequence + 1

        super(TensorboardJob, self).save(*args, **kwargs)

    @property
    def unique_name(self):
        return '{}.tensorboards.{}'.format(self.project.unique_name, self.sequence)

    @cached_property
    def image(self):
        return self.specification.run_exec.image

    def set_status(self, status, message=None, details=None):  # pylint:disable=arguments-differ
        return self._set_status(status_model=TensorboardJobStatus,
                                logger=_logger,
                                status=status,
                                message=message,
                                details=details)


class TensorboardJobStatus(AbstractJobStatus):
    """A model that represents tensorboard job status at certain time."""
    job = models.ForeignKey(
        'db.TensorboardJob',
        on_delete=models.CASCADE,
        related_name='statuses')

    class Meta(AbstractJobStatus.Meta):
        app_label = 'db'
        verbose_name_plural = 'Tensorboard Job Statuses'
