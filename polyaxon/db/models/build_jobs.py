import logging

from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.functional import cached_property
from polyaxon_schemas.run_exec import BuildConfig

from db.models.jobs import Job, JobStatus
from libs.spec_validation import validate_build_config

logger = logging.getLogger('db.build_jobs')


class BuildJob(Job):
    """A model that represents the configuration for build job."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='+')
    project = models.ForeignKey(
        'db.Project',
        on_delete=models.CASCADE,
        related_name='build_jobs')
    config = JSONField(
        help_text='The compiled polyaxonfile for plugin job.',
        validators=[validate_build_config])
    code_reference = models.ForeignKey(
        'db.CodeReference',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='+')
    job_status = models.OneToOneField(
        'db.BuildJobStatus',
        related_name='+',
        blank=True,
        null=True,
        editable=True,
        on_delete=models.SET_NULL)

    class Meta:
        app_label = 'db'

    def __str__(self):
        return '{} build<{}, ref({})>'.format(self.project, self.image, self.code_reference)

    @cached_property
    def specification(self):
        return BuildConfig.from_dict(self.config)

    @cached_property
    def image(self):
        return self.specification.image

    @cached_property
    def build_steps(self):
        return self.specification.build_steps

    @cached_property
    def env_vars(self):
        return self.specification.env_vars

    @cached_property
    def unique_name(self):
        return self.__str__()

    def set_status(self, status, message=None, details=None):  # pylint:disable=arguments-differ
        return self._set_status(status_model=BuildJobStatus,
                                logger=logger,
                                status=status,
                                message=message,
                                details=details)


class BuildJobStatus(JobStatus):
    """A model that represents build job status at certain time."""
    job = models.ForeignKey(
        'db.BuildJob',
        on_delete=models.CASCADE,
        related_name='statuses')

    class Meta(JobStatus.Meta):
        app_label = 'db'
        verbose_name_plural = 'Build Job Statuses'
