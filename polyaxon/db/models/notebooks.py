from typing import Dict

from hestia.datetime_typing import AwareDT

from django.db import models
from django.utils.functional import cached_property

from constants.k8s_jobs import JOB_NAME_FORMAT, NOTEBOOK_JOB_NAME
from db.models.abstract.backend import BackendModel
from db.models.abstract.datarefs import DataReferenceModel
from db.models.abstract.job import AbstractJobStatusModel, JobMixin
from db.models.plugins import PluginJobBase
from db.models.unique_names import NOTEBOOK_UNIQUE_NAME_FORMAT
from libs.paths.jobs import get_job_subpath
from libs.spec_validation import validate_notebook_spec_config
from schemas import NotebookSpecification


class NotebookJob(PluginJobBase, BackendModel, DataReferenceModel, JobMixin):
    """A model that represents the configuration for tensorboard job."""
    JOBS_NAME = 'notebooks'

    project = models.ForeignKey(
        'db.Project',
        on_delete=models.CASCADE,
        related_name='notebook_jobs')
    content = models.TextField(
        null=True,
        blank=True,
        help_text='The yaml content of the polyaxonfile/specification.',
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
    def unique_name(self) -> str:
        return NOTEBOOK_UNIQUE_NAME_FORMAT.format(
            project_name=self.project.unique_name,
            id=self.id)

    @cached_property
    def subpath(self) -> str:
        return get_job_subpath(job_name=self.unique_name)

    @cached_property
    def pod_id(self) -> str:
        return JOB_NAME_FORMAT.format(name=NOTEBOOK_JOB_NAME, job_uuid=self.uuid.hex)

    @cached_property
    def specification(self) -> 'NotebookSpecification':
        return NotebookSpecification(values=self.content) if self.content else None

    @property
    def has_specification(self) -> bool:
        return self.content is not None

    def set_status(self,  # pylint:disable=arguments-differ
                   status: str,
                   created_at: AwareDT = None,
                   message: str = None,
                   traceback: Dict = None,
                   details: Dict = None) -> bool:
        params = {'created_at': created_at} if created_at else {}
        return self._set_status(status_model=NotebookJobStatus,
                                status=status,
                                message=message,
                                traceback=traceback,
                                details=details,
                                **params)


class NotebookJobStatus(AbstractJobStatusModel):
    """A model that represents notebook job status at certain time."""
    job = models.ForeignKey(
        'db.NotebookJob',
        on_delete=models.CASCADE,
        related_name='statuses')

    class Meta(AbstractJobStatusModel.Meta):
        app_label = 'db'
        verbose_name_plural = 'Notebook Job Statuses'
