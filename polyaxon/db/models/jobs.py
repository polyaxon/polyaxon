from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.functional import cached_property

import auditor

from db.models.abstract_jobs import AbstractJob, AbstractJobStatus, JobMixin
from db.models.cloning_strategies import CloningStrategy
from db.models.utils import DescribableModel, NameableModel, PersistenceModel, TagModel
from event_manager.events.job import JOB_RESTARTED
from libs.spec_validation import validate_job_spec_config
from polyaxon_schemas.polyaxonfile.specification import JobSpecification


class Job(AbstractJob, PersistenceModel, NameableModel, DescribableModel, TagModel, JobMixin):
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
    original_job = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='clones',
        help_text='The original job that was cloned from.')
    cloning_strategy = models.CharField(
        max_length=16,
        blank=True,
        null=True,
        default=CloningStrategy.RESTART,
        choices=CloningStrategy.CHOICES)
    status = models.OneToOneField(
        'db.JobStatus',
        related_name='+',
        blank=True,
        null=True,
        editable=True,
        on_delete=models.SET_NULL)

    class Meta:
        app_label = 'db'
        unique_together = (('project', 'name'),)

    @cached_property
    def unique_name(self):
        return '{}.jobs.{}'.format(self.project.unique_name, self.id)

    @cached_property
    def specification(self):
        return JobSpecification(values=self.config)

    @property
    def is_clone(self):
        return self.original_job is not None

    @property
    def original_unique_name(self):
        return self.original_job.unique_name if self.original_job else None

    @property
    def is_restart(self):
        return self.is_clone and self.cloning_strategy == CloningStrategy.RESTART

    @property
    def is_resume(self):
        return self.is_clone and self.cloning_strategy == CloningStrategy.RESUME

    @property
    def is_copy(self):
        return self.is_clone and self.cloning_strategy == CloningStrategy.COPY

    def set_status(self, status, message=None, details=None):  # pylint:disable=arguments-differ
        return self._set_status(status_model=JobStatus,
                                status=status,
                                message=message,
                                details=details)

    def _clone(self,
               cloning_strategy,
               event_type,
               user=None,
               description=None,
               config=None,
               code_reference=None,
               update_code_reference=False):
        if not code_reference and not update_code_reference:
            code_reference = self.code_reference
        instance = Job.objects.create(
            project=self.project,
            user=user or self.user,
            description=description or self.description,
            config=config or self.config,
            original_job=self,
            cloning_strategy=cloning_strategy,
            code_reference=code_reference)
        auditor.record(event_type=event_type, instance=instance)
        return instance

    def restart(self,
                user=None,
                description=None,
                config=None,
                code_reference=None,
                update_code_reference=False):
        return self._clone(cloning_strategy=CloningStrategy.RESTART,
                           event_type=JOB_RESTARTED,
                           user=user,
                           description=description,
                           config=config,
                           code_reference=code_reference,
                           update_code_reference=update_code_reference)


class JobStatus(AbstractJobStatus):
    """A model that represents run job status at certain time."""
    job = models.ForeignKey(
        'db.Job',
        on_delete=models.CASCADE,
        related_name='statuses')

    class Meta(AbstractJobStatus.Meta):
        app_label = 'db'
        verbose_name_plural = 'Job Statuses'
