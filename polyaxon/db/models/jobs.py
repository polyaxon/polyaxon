import logging

from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.functional import cached_property

from db.models.abstract_jobs import AbstractJob, AbstractJobStatus
from libs.spec_validation import validate_job_spec_config
from polyaxon_schemas.polyaxonfile.specification import JobSpecification

logger = logging.getLogger('db.build_jobs')


class Job(AbstractJob):
    """A model that represents the configuration for run job."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='+')
    project = models.ForeignKey(
        'db.Project',
        on_delete=models.CASCADE,
        related_name='jobs')
    config = JSONField(
        help_text='The compiled polyaxonfile for the run job.',
        validators=[validate_job_spec_config])
    code_reference = models.ForeignKey(
        'db.CodeReference',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='+')
    build_job = models.ForeignKey(
        'db.BuildJob',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='+')
    status = models.OneToOneField(
        'db.JobStatus',
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
            last = Job.objects.filter(project=self.project).last()
            self.sequence = 1
            if last:
                self.sequence = last.sequence + 1

        super(Job, self).save(*args, **kwargs)

    @property
    def unique_name(self):
        return '{}.jobs.{}'.format(self.project.unique_name, self.sequence)

    @cached_property
    def specification(self):
        return JobSpecification(values=self.config)

    @cached_property
    def image(self):
        return self.specification.build.image

    @cached_property
    def build_steps(self):
        return self.specification.build.build_steps

    @cached_property
    def resources(self):
        return None

    @cached_property
    def node_selectors(self):
        return None

    @cached_property
    def env_vars(self):
        return self.specification.build.env_vars

    def set_status(self, status, message=None, details=None):  # pylint:disable=arguments-differ
        return self._set_status(status_model=JobStatus,
                                logger=logger,
                                status=status,
                                message=message,
                                details=details)


class JobStatus(AbstractJobStatus):
    """A model that represents run job status at certain time."""
    job = models.ForeignKey(
        'db.Job',
        on_delete=models.CASCADE,
        related_name='statuses')

    class Meta(AbstractJobStatus.Meta):
        app_label = 'db'
        verbose_name_plural = 'Run Job Statuses'
