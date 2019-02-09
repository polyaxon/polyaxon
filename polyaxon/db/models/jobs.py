from typing import Dict, Optional

from hestia.datetime_typing import AwareDT

from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.functional import cached_property

import auditor

from constants.k8s_jobs import JOB_NAME, JOB_NAME_FORMAT
from db.models.abstract_jobs import AbstractJob, AbstractJobStatus, JobMixin
from db.models.cloning_strategies import CloningStrategy
from db.models.unique_names import JOB_UNIQUE_NAME_FORMAT
from db.models.utils import (
    DataReference,
    DeletedModel,
    DescribableModel,
    InCluster,
    NameableModel,
    NodeSchedulingModel,
    OutputsModel,
    PersistenceModel,
    ReadmeModel,
    SubPathModel,
    TagModel
)
from db.redis.heartbeat import RedisHeartBeat
from event_manager.events.job import JOB_RESTARTED
from libs.paths.jobs import get_job_subpath
from libs.spec_validation import validate_job_spec_config
from schemas.specifications import JobSpecification


class Job(AbstractJob,
          InCluster,
          DataReference,
          OutputsModel,
          PersistenceModel,
          SubPathModel,
          NodeSchedulingModel,
          NameableModel,
          DescribableModel,
          ReadmeModel,
          TagModel,
          DeletedModel,
          JobMixin):
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
        related_name='jobs')
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
    def unique_name(self) -> str:
        return JOB_UNIQUE_NAME_FORMAT.format(
            project_name=self.project.unique_name,
            id=self.id)

    @property
    def subpath(self) -> str:
        return get_job_subpath(job_name=self.unique_name)

    @cached_property
    def pod_id(self) -> str:
        return JOB_NAME_FORMAT.format(name=JOB_NAME, job_uuid=self.uuid.hex)

    @cached_property
    def specification(self) -> 'JobSpecification':
        return JobSpecification(values=self.config)

    @property
    def has_specification(self) -> bool:
        return self.config is not None

    @property
    def is_clone(self) -> bool:
        return self.original_job is not None

    @property
    def original_unique_name(self) -> Optional[str]:
        return self.original_job.unique_name if self.original_job else None

    @property
    def is_restart(self) -> bool:
        return self.is_clone and self.cloning_strategy == CloningStrategy.RESTART

    @property
    def is_resume(self) -> bool:
        return self.is_clone and self.cloning_strategy == CloningStrategy.RESUME

    @property
    def is_copy(self) -> bool:
        return self.is_clone and self.cloning_strategy == CloningStrategy.COPY

    def _ping_heartbeat(self) -> None:
        RedisHeartBeat.job_ping(self.id)

    def set_status(self,  # pylint:disable=arguments-differ
                   status: str,
                   created_at: AwareDT = None,
                   message: str = None,
                   traceback: Dict = None,
                   details: Dict = None) -> bool:
        params = {'created_at': created_at} if created_at else {}
        return self._set_status(status_model=JobStatus,
                                status=status,
                                message=message,
                                details=details,
                                **params)

    def _clone(self,
               cloning_strategy: str,
               event_type: str,
               user=None,
               description: str = None,
               config=None,
               code_reference=None,
               update_code_reference: bool = False) -> 'Job':
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
                description: str = None,
                config=None,
                code_reference=None,
                update_code_reference: bool = False) -> 'Job':
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
