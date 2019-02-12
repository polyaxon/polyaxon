from typing import Dict, Tuple

from hestia.datetime_typing import AwareDT

from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.functional import cached_property

import conf

from constants.images_tags import LATEST_IMAGE_TAG
from constants.k8s_jobs import DOCKERIZER_JOB_NAME, JOB_NAME_FORMAT
from db.models.abstract_jobs import AbstractJob, AbstractJobStatus, JobMixin
from db.models.unique_names import BUILD_UNIQUE_NAME_FORMAT
from db.models.utils import (
    DeletedModel,
    DescribableModel,
    InCluster,
    NameableModel,
    NodeSchedulingModel,
    PersistenceModel,
    SubPathModel,
    TagModel
)
from db.redis.heartbeat import RedisHeartBeat
from libs.paths.jobs import get_job_subpath
from libs.spec_validation import validate_build_spec_config
from schemas.build_backends import BuildBackend
from schemas.specifications import BuildSpecification


class BuildJob(AbstractJob,
               InCluster,
               NodeSchedulingModel,
               NameableModel,
               DescribableModel,
               PersistenceModel,
               SubPathModel,
               TagModel,
               DeletedModel,
               JobMixin):
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
        help_text='The compiled polyaxonfile for the build job.',
        validators=[validate_build_spec_config])
    code_reference = models.ForeignKey(
        'db.CodeReference',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='+')
    backend = models.CharField(
        max_length=16,
        blank=True,
        null=True,
        default=BuildBackend.NATIVE)
    dockerfile = models.TextField(
        blank=True,
        null=True,
        help_text='The dockerfile used to create the image with this job.')
    status = models.OneToOneField(
        'db.BuildJobStatus',
        related_name='+',
        blank=True,
        null=True,
        editable=True,
        on_delete=models.SET_NULL)

    class Meta:
        app_label = 'db'
        unique_together = (('project', 'name'),)

    @cached_property
    def commit(self):
        if self.code_reference:
            return self.code_reference.commit
        return None

    @cached_property
    def unique_name(self) -> str:
        return BUILD_UNIQUE_NAME_FORMAT.format(
            project_name=self.project.unique_name,
            id=self.id)

    @cached_property
    def subpath(self) -> str:
        return get_job_subpath(job_name=self.unique_name)

    @cached_property
    def pod_id(self) -> str:
        return JOB_NAME_FORMAT.format(name=DOCKERIZER_JOB_NAME, job_uuid=self.uuid.hex)

    @cached_property
    def specification(self) -> 'BuildSpecification':
        return BuildSpecification(values=self.config)

    @property
    def has_specification(self) -> bool:
        return self.config is not None

    def _ping_heartbeat(self) -> None:
        RedisHeartBeat.build_ping(self.id)

    def set_status(self,  # pylint:disable=arguments-differ
                   status: str,
                   created_at: AwareDT = None,
                   message: str = None,
                   traceback: Dict = None,
                   details: Dict = None) -> bool:
        params = {'created_at': created_at} if created_at else {}
        return self._set_status(status_model=BuildJobStatus,
                                status=status,
                                message=message,
                                traceback=traceback,
                                details=details,
                                **params)

    @staticmethod
    def create(user,
               project,
               config,
               code_reference,
               configmap_refs=None,
               secret_refs=None,
               nocache=False) -> Tuple['BuildJob', bool]:
        build_config = BuildSpecification.create_specification(config,
                                                               configmap_refs=configmap_refs,
                                                               secret_refs=secret_refs,
                                                               to_dict=False)
        if not nocache and build_config.build.nocache is not None:
            # Set the config's nocache rebuild
            nocache = build_config.build.nocache
        # Check if image is not using latest tag, then we can reuse a previous build
        rebuild_cond = (
            nocache or
            (conf.get('BUILD_ALWAYS_PULL_LATEST') and
             build_config.build.image_tag == LATEST_IMAGE_TAG)
        )
        if not rebuild_cond:
            job = BuildJob.objects.filter(project=project,
                                          config=build_config.parsed_data,
                                          code_reference=code_reference).last()
            if job:
                return job, False

        return BuildJob.objects.create(user=user,
                                       project=project,
                                       config=build_config.parsed_data,
                                       code_reference=code_reference), True


class BuildJobStatus(AbstractJobStatus):
    """A model that represents build job status at certain time."""
    job = models.ForeignKey(
        'db.BuildJob',
        on_delete=models.CASCADE,
        related_name='statuses')

    class Meta(AbstractJobStatus.Meta):
        app_label = 'db'
        verbose_name_plural = 'Build Job Statuses'
