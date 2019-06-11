from typing import Dict, Optional

from hestia.datetime_typing import AwareDT

from django.conf import settings
from django.db import models
from django.utils.functional import cached_property

import auditor

from constants.cloning_strategies import CloningStrategy
from constants.k8s_jobs import JOB_NAME, JOB_NAME_FORMAT
from db.models.abstract.backend import BackendModel
from db.models.abstract.datarefs import DataReferenceModel
from db.models.abstract.deleted import DeletedModel
from db.models.abstract.describable import DescribableModel
from db.models.abstract.is_managed import IsManagedModel
from db.models.abstract.job import AbstractJobModel, AbstractJobStatusModel, JobMixin
from db.models.abstract.nameable import NameableModel
from db.models.abstract.node_scheduling import NodeSchedulingModel
from db.models.abstract.outputs import OutputsModel
from db.models.abstract.persistence import PersistenceModel
from db.models.abstract.readme import ReadmeModel
from db.models.abstract.sub_paths import SubPathModel
from db.models.abstract.tag import TagModel
from db.models.unique_names import JOB_UNIQUE_NAME_FORMAT
from db.redis.heartbeat import RedisHeartBeat
from events.registry.job import JOB_RESTARTED
from libs.paths.jobs import get_job_subpath
from libs.spec_validation import validate_job_spec_config
from schemas import JobSpecification


class Job(AbstractJobModel,
          BackendModel,
          IsManagedModel,
          DataReferenceModel,
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
    content = models.TextField(
        null=True,
        blank=True,
        help_text='The yaml content of the polyaxonfile/specification.',
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
        return JobSpecification(values=self.content) if self.content else None

    @property
    def has_specification(self) -> bool:
        return self.content is not None

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
               content=None,
               code_reference=None,
               update_code_reference: bool = False) -> 'Job':
        if not code_reference and not update_code_reference:
            code_reference = self.code_reference
        instance = Job.objects.create(
            project=self.project,
            user=user or self.user,
            description=description or self.description,
            content=content or self.content,
            original_job=self,
            cloning_strategy=cloning_strategy,
            code_reference=code_reference)
        auditor.record(event_type=event_type, instance=instance)
        return instance

    def restart(self,
                user=None,
                description: str = None,
                content=None,
                code_reference=None,
                update_code_reference: bool = False) -> 'Job':
        return self._clone(cloning_strategy=CloningStrategy.RESTART,
                           event_type=JOB_RESTARTED,
                           user=user,
                           description=description,
                           content=content,
                           code_reference=code_reference,
                           update_code_reference=update_code_reference)


class JobStatus(AbstractJobStatusModel):
    """A model that represents run job status at certain time."""
    job = models.ForeignKey(
        'db.Job',
        on_delete=models.CASCADE,
        related_name='statuses')

    class Meta(AbstractJobStatusModel.Meta):
        app_label = 'db'
        verbose_name_plural = 'Job Statuses'
