from typing import Dict

from hestia.datetime_typing import AwareDT

from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.functional import cached_property

from constants.k8s_jobs import JOB_NAME_FORMAT, NOTEBOOK_JOB_NAME
from db.models.abstract_jobs import AbstractJobStatus, JobMixin
from db.models.plugins import PluginJobBase
from db.models.unique_names import NOTEBOOK_UNIQUE_NAME_FORMAT
from db.models.utils import DataReference
from libs.paths.jobs import get_job_subpath
from libs.spec_validation import validate_notebook_spec_config
from schemas.specifications import NotebookSpecification


class NotebookJob(PluginJobBase, DataReference, JobMixin):
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
        return NotebookSpecification(values=self.config)

    @property
    def has_specification(self) -> bool:
        return self.config is not None

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


class NotebookJobStatus(AbstractJobStatus):
    """A model that represents notebook job status at certain time."""
    job = models.ForeignKey(
        'db.NotebookJob',
        on_delete=models.CASCADE,
        related_name='statuses')

    class Meta(AbstractJobStatus.Meta):
        app_label = 'db'
        verbose_name_plural = 'Notebook Job Statuses'
