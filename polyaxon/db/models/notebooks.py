from django.contrib.postgres.fields import JSONField
from django.db import models

from db.models.abstract_jobs import AbstractJobStatus, JobMixin
from db.models.plugins import PluginJobBase
from db.models.utils import NameableModel
from libs.spec_validation import validate_notebook_spec_config
from polyaxon_schemas.polyaxonfile.specification import NotebookSpecification
from polyaxon_schemas.polyaxonfile.utils import cached_property


class NotebookJob(PluginJobBase, JobMixin):
    """A model that represents the configuration for tensorboard job."""
    JOBS_NAME = 'notebooks'

    project = models.ForeignKey(
        'db.Project',
        on_delete=models.CASCADE,
        related_name='notebook_jobs')
    config = JSONField(
        help_text='The compiled polyaxonfile for the notebook job.',
        validators=[validate_notebook_spec_config])
    status = models.OneToOneField(
        'db.NotebookJobStatus',
        related_name='+',
        blank=True,
        null=True,
        editable=True,
        on_delete=models.SET_NULL)

    class Meta:
        app_label = 'db'

    @cached_property
    def unique_name(self):
        return '{}.notebooks.{}'.format(self.project.unique_name, self.id)

    @cached_property
    def specification(self):
        return NotebookSpecification(values=self.config)

    def set_status(self, status, message=None, details=None):  # pylint:disable=arguments-differ
        return self._set_status(status_model=NotebookJobStatus,
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
