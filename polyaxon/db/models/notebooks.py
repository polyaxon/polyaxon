import logging

from django.db import models

from db.models.abstract_jobs import AbstractJobStatus
from db.models.plugins import PluginJobBase

_logger = logging.getLogger('db.notebooks')


class NotebookJob(PluginJobBase):
    """A model that represents the configuration for tensorboard job."""
    JOBS_NAME = 'notebooks'

    project = models.ForeignKey(
        'db.Project',
        on_delete=models.CASCADE,
        related_name='notebook_jobs')
    status = models.OneToOneField(
        'db.NotebookJobStatus',
        related_name='+',
        blank=True,
        null=True,
        editable=True,
        on_delete=models.SET_NULL)

    class Meta:
        app_label = 'db'

    def __str__(self):
        return '{} notebook'.format(self.project)

    def save(self, *args, **kwargs):  # pylint:disable=arguments-differ
        if self.pk is None:
            last = NotebookJob.objects.filter(project=self.project).last()
            self.sequence = 1
            if last:
                self.sequence = last.sequence + 1

        super(NotebookJob, self).save(*args, **kwargs)

    @property
    def unique_name(self):
        return '{}.notebooks.{}'.format(self.project.unique_name, self.sequence)

    def set_status(self, status, message=None, details=None):  # pylint:disable=arguments-differ
        return self._set_status(status_model=NotebookJobStatus,
                                logger=_logger,
                                status=status,
                                message=message,
                                details=details)


class NotebookJobStatus(AbstractJobStatus):
    """A model that represents notebook job status at certain time."""
    job = models.ForeignKey(
        'db.NotebookJob',
        on_delete=models.CASCADE,
        related_name='statuses')

    class Meta(AbstractJobStatus.Meta):
        app_label = 'db'
        verbose_name_plural = 'Notebook Job Statuses'
