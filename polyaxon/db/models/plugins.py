import logging

from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.functional import cached_property

from db.models.jobs import Job, JobStatus
from libs.spec_validation import validate_plugin_spec_config
from polyaxon_schemas.polyaxonfile.specification import PluginSpecification

logger = logging.getLogger('db.plugins')


class PluginJobBase(Job):
    """A base model for plugin jobs."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='+')
    config = JSONField(
        help_text='The compiled polyaxonfile for plugin job.',
        validators=[validate_plugin_spec_config])
    code_reference = models.ForeignKey(
        'db.CodeReference',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='+')

    class Meta:
        app_label = 'db'
        abstract = True

    @cached_property
    def specification(self):
        return PluginSpecification(values=self.config)

    @cached_property
    def resources(self):
        return self.specification.resources

    @cached_property
    def node_selectors(self):
        return self.specification.node_selectors

    @cached_property
    def unique_name(self):
        return self.__str__()

    def _set_status(self, status_model, logger, status, message=None, details=None):
        # pylint:disable=redefined-outer-name
        current_status = self.last_status
        if status != current_status:
            # Add new status to the job
            status_model.objects.create(job=self,
                                        status=status,
                                        message=message,
                                        details=details)
            return True
        return False


class TensorboardJob(PluginJobBase):
    """A model that represents the configuration for tensorboard job."""
    project = models.ForeignKey(
        'db.Project',
        on_delete=models.CASCADE,
        related_name='tensorboard_jobs')
    job_status = models.OneToOneField(
        'db.TensorboardJobStatus',
        related_name='+',
        blank=True,
        null=True,
        editable=True,
        on_delete=models.SET_NULL)

    class Meta:
        app_label = 'db'

    def __str__(self):
        return '{} tensorboard<{}>'.format(self.project, self.image)

    @cached_property
    def image(self):
        return self.specification.run_exec.image

    def set_status(self, status, message=None, details=None):  # pylint:disable=arguments-differ
        return self._set_status(status_model=TensorboardJobStatus,
                                logger=logger,
                                status=status,
                                message=message,
                                details=details)


class NotebookJob(PluginJobBase):
    """A model that represents the configuration for tensorboard job."""
    project = models.ForeignKey(
        'db.Project',
        on_delete=models.CASCADE,
        related_name='notebook_jobs')
    job_status = models.OneToOneField(
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

    def set_status(self, status, message=None, details=None):  # pylint:disable=arguments-differ
        return self._set_status(status_model=NotebookJobStatus,
                                logger=logger,
                                status=status,
                                message=message,
                                details=details)


class TensorboardJobStatus(JobStatus):
    """A model that represents tensorboard job status at certain time."""
    job = models.ForeignKey(
        'db.TensorboardJob',
        on_delete=models.CASCADE,
        related_name='statuses')

    class Meta(JobStatus.Meta):
        app_label = 'db'
        verbose_name_plural = 'Tensorboard Job Statuses'


class NotebookJobStatus(JobStatus):
    """A model that represents notebook job status at certain time."""
    job = models.ForeignKey(
        'db.NotebookJob',
        on_delete=models.CASCADE,
        related_name='statuses')

    class Meta(JobStatus.Meta):
        app_label = 'db'
        verbose_name_plural = 'Notebook Job Statuses'
