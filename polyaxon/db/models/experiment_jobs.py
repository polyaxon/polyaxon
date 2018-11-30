from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.functional import cached_property

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
    def unique_name(self):
        return EXPERIMENT_JOB_UNIQUE_NAME_FORMAT.format(
            experiment_name=self.experiment.unique_name,
            id=self.id,
            role=self.role
        )

    def set_status(self,  # pylint:disable=arguments-differ
                   status,
                   created_at=None,
                   message=None,
                   traceback=None,
                   details=None):
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
