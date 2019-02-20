import logging
import uuid

from typing import Dict, List, Optional

from hestia.datetime_typing import AwareDT

from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.functional import cached_property

from constants.jobs import JobLifeCycle
from db.models.statuses import LastStatusMixin, StatusModel
from db.models.utils import CachedMixin, DiffModel, RunTimeModel
from schemas.pod_resources import PodResourcesConfig

_logger = logging.getLogger('polyaxon.db.jobs')


class AbstractJob(DiffModel, RunTimeModel, LastStatusMixin):
    """An abstract base class for job, used both by experiment jobs and other jobs."""
    STATUSES = JobLifeCycle

    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        null=False)
    definition = JSONField(help_text='The specific values/manifest for this job.',
                           default=dict)

    class Meta:
        abstract = True

    def _ping_heartbeat(self):
        """Run's heartbeat callback."""
        pass

    def last_status_before(self,  # pylint:disable=arguments-differ
                           status_model,
                           status_date: AwareDT = None) -> Optional[str]:
        if not status_date:
            return self.last_status
        status = status_model.objects.filter(job=self, created_at__lte=status_date).last()
        return status.status if status else None

    def _set_status(self,
                    status_model,
                    status: str,
                    created_at: AwareDT = None,
                    message: str = None,
                    traceback: Dict = None,
                    details: Dict = None) -> bool:
        current_status = self.last_status_before(status_model=status_model, status_date=created_at)
        if self.is_done:
            # We should not update statuses anymore
            _logger.debug(
                'Received a new status `%s` for job `%s`. '
                'But the job is already done with status `%s`',
                status, self.unique_name, current_status)
            return False
        if status in JobLifeCycle.HEARTBEAT_STATUS:
            self._ping_heartbeat()
        if JobLifeCycle.can_transition(status_from=current_status, status_to=status):
            # Add new status to the job
            params = {'created_at': created_at} if created_at else {}
            status_model.objects.create(job=self,
                                        status=status,
                                        message=message,
                                        traceback=traceback,
                                        details=details,
                                        **params)
            return True
        return False


class JobMixin(object):

    def __str__(self) -> str:
        return self.unique_name

    @cached_property
    def unique_name(self) -> str:
        pass

    @cached_property
    def secret_refs(self) -> Optional[List[str]]:
        return self.specification.secret_refs

    @cached_property
    def configmap_refs(self) -> Optional[List[str]]:
        return self.specification.configmap_refs

    @cached_property
    def resources(self) -> Optional[PodResourcesConfig]:
        return self.specification.resources

    @cached_property
    def node_selector(self) -> Optional[Dict]:
        return self.specification.node_selector

    @cached_property
    def affinity(self) -> Optional[Dict]:
        return self.specification.affinity

    @cached_property
    def tolerations(self) -> Optional[List[Dict]]:
        return self.specification.tolerations

    @cached_property
    def build_image(self) -> str:
        return self.specification.build.image

    @cached_property
    def build_dockerfile(self) -> str:
        return self.specification.build.dockerfile

    @cached_property
    def build_context(self) -> str:
        return self.specification.build.context

    @cached_property
    def build_steps(self) -> List[str]:
        return self.specification.build.build_steps

    @cached_property
    def build_env_vars(self) -> Optional[List[str]]:
        return self.specification.build.env_vars


class TensorboardJobMixin(CachedMixin):
    CACHED_PROPERTIES = ['tensorboard', 'has_tensorboard']

    @cached_property
    def tensorboard(self) -> 'TensorboardJob':
        return self.tensorboard_jobs.last()

    @cached_property
    def has_tensorboard(self) -> bool:
        tensorboard = self.tensorboard
        return tensorboard and tensorboard.is_stoppable


class AbstractJobStatus(StatusModel):
    """A model that represents job status at certain time."""
    STATUSES = JobLifeCycle

    status = models.CharField(
        max_length=64,
        blank=True,
        null=True,
        default=STATUSES.CREATED,
        choices=STATUSES.CHOICES)
    details = JSONField(null=True, blank=True, default=dict)

    def __str__(self) -> str:
        return '{} <{}>'.format(self.job.unique_name, self.status)

    class Meta:
        verbose_name_plural = 'Job Statuses'
        ordering = ['created_at']
        abstract = True
