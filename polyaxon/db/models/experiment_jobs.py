from typing import Dict

from hestia.datetime_typing import AwareDT

from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.functional import cached_property

from constants.k8s_jobs import EXPERIMENT_JOB_NAME_FORMAT
from db.models.abstract_jobs import AbstractJob, AbstractJobStatus
from db.models.unique_names import EXPERIMENT_JOB_UNIQUE_NAME_FORMAT
from db.models.utils import NodeSchedulingModel
from schemas.tasks import TaskType


class ExperimentJob(AbstractJob, NodeSchedulingModel):
    """A model that represents job related to an experiment"""
    experiment = models.ForeignKey(
        'db.Experiment',
        on_delete=models.CASCADE,
        related_name='jobs')
    role = models.CharField(max_length=64, default=TaskType.MASTER)
    sequence = models.IntegerField(null=True, blank=True, default=0)
    resources = models.OneToOneField(
        'db.JobResources',
        related_name='+',
        blank=True,
        null=True,
        editable=True,
        on_delete=models.SET_NULL)
    node_selector = JSONField(
        null=True,
        blank=True)
    affinity = JSONField(
        null=True,
        blank=True)
    tolerations = JSONField(
        blank=True,
        null=True)
    status = models.OneToOneField(
        'db.ExperimentJobStatus',
        related_name='+',
        blank=True,
        null=True,
        editable=True,
        on_delete=models.SET_NULL)

    class Meta:
        app_label = 'db'

    @cached_property
    def unique_name(self) -> str:
        return EXPERIMENT_JOB_UNIQUE_NAME_FORMAT.format(
            experiment_name=self.experiment.unique_name,
            id=self.id,
            role=self.role
        )

    @cached_property
    def pod_id(self) -> str:
        return EXPERIMENT_JOB_NAME_FORMAT.format(
            task_type=self.role,
            task_idx=self.sequence,
            experiment_uuid=self.experiment.uuid.hex
        )

    def set_status(self,  # pylint:disable=arguments-differ
                   status: str,
                   created_at: AwareDT = None,
                   message: str = None,
                   traceback: Dict = None,
                   details: Dict = None) -> bool:
        params = {'created_at': created_at} if created_at else {}
        return self._set_status(status_model=ExperimentJobStatus,
                                status=status,
                                message=message,
                                traceback=traceback,
                                details=details,
                                **params)


class ExperimentJobStatus(AbstractJobStatus):
    """A model that represents job status at certain time."""
    job = models.ForeignKey(
        'db.ExperimentJob',
        on_delete=models.CASCADE,
        related_name='statuses')

    class Meta(AbstractJobStatus.Meta):
        app_label = 'db'
        verbose_name_plural = 'Experiment Job Statuses'
