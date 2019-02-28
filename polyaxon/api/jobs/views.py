import logging
import os

from hestia.bool_utils import to_bool
from polystores.exceptions import PolyaxonStoresException
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.settings import api_settings

import auditor
import conf
import stores

from api.endpoint.base import (
    CreateEndpoint,
    DestroyEndpoint,
    ListEndpoint,
    PostEndpoint,
    RetrieveEndpoint,
    UpdateEndpoint
)
from api.endpoint.job import JobEndpoint, JobResourceEndpoint, JobResourceListEndpoint
from api.endpoint.project import ProjectResourceListEndpoint
from api.filters import OrderingFilter, QueryFilter
from api.jobs import queries
from api.jobs.serializers import (
    BookmarkedJobSerializer,
    JobCreateSerializer,
    JobDetailSerializer,
    JobSerializer,
    JobStatusSerializer
)
from api.utils.files import stream_file
from api.utils.views.bookmarks_mixin import BookmarkedListMixinView
from api.utils.views.protected import ProtectedView
from constants.jobs import JobLifeCycle
from db.models.jobs import Job, JobStatus
from db.models.tokens import Token
from db.redis.heartbeat import RedisHeartBeat
from db.redis.tll import RedisTTL
from event_manager.events.job import (
    JOB_ARCHIVED,
    JOB_DELETED_TRIGGERED,
    JOB_LOGS_VIEWED,
    JOB_OUTPUTS_DOWNLOADED,
    JOB_RESTARTED_TRIGGERED,
    JOB_RESTORED,
    JOB_STATUSES_VIEWED,
    JOB_STOPPED_TRIGGERED,
    JOB_UPDATED,
    JOB_VIEWED
)
from event_manager.events.project import PROJECT_JOBS_VIEWED
from libs.archive import archive_logs_file, archive_outputs, archive_outputs_file
from libs.spec_validation import validate_job_spec_config
from logs_handlers.log_queries.job import process_logs
from polyaxon.celery_api import celery_app
from polyaxon.settings import SchedulerCeleryTasks
from scopes.authentication.internal import InternalAuthentication
from scopes.permissions.internal import IsAuthenticatedOrInternal, IsInitializer
from scopes.permissions.projects import get_permissible_project
from stores.exceptions import VolumeNotFoundError  # noqa

_logger = logging.getLogger("polyaxon.views.jobs")


class ProjectJobListView(BookmarkedListMixinView,
                         ProjectResourceListEndpoint,
                         ListEndpoint,
                         CreateEndpoint):
    """
    get:
        List jobs under a project.

    post:
        Create a job under a project.
    """
    queryset = queries.jobs
    serializer_class = BookmarkedJobSerializer
    create_serializer_class = JobCreateSerializer
    filter_backends = (QueryFilter, OrderingFilter,)
    query_manager = 'job'
    ordering = ('-updated_at',)
    ordering_fields = ('created_at', 'updated_at', 'started_at', 'finished_at')

    def filter_queryset(self, queryset):
        auditor.record(event_type=PROJECT_JOBS_VIEWED,
                       instance=self.project,
                       actor_id=self.request.user.id,
                       actor_name=self.request.user.username)
        return super().filter_queryset(queryset=queryset)

    def perform_create(self, serializer):
        ttl = self.request.data.get(RedisTTL.TTL_KEY)
        if ttl:
            try:
                ttl = RedisTTL.validate_ttl(ttl)
            except ValueError:
                raise ValidationError('ttl must be an integer.')
        instance = serializer.save(user=self.request.user,
                                   project=self.project)
        if ttl:
            RedisTTL.set_for_job(job_id=instance.id, value=ttl)


class JobDetailView(JobEndpoint, RetrieveEndpoint, UpdateEndpoint, DestroyEndpoint):
    """
    get:
        Get a job details.
    patch:
        Update a job details.
    delete:
        Delete a job.
    """
    queryset = queries.jobs_details
    serializer_class = JobDetailSerializer
    instance = None
    AUDITOR_EVENT_TYPES = {
        'GET': JOB_VIEWED,
        'UPDATE': JOB_UPDATED,
        'DELETE': JOB_DELETED_TRIGGERED
    }

    def perform_destroy(self, instance):
        instance.archive()
        celery_app.send_task(
            SchedulerCeleryTasks.JOBS_SCHEDULE_DELETION,
            kwargs={'job_id': instance.id, 'immediate': True},
            countdown=conf.get('GLOBAL_COUNTDOWN'))


class JobArchiveView(JobEndpoint, CreateEndpoint):
    """Restore an Build."""
    serializer_class = JobSerializer

    def post(self, request, *args, **kwargs):
        obj = self.get_object()
        auditor.record(event_type=JOB_ARCHIVED,
                       instance=obj,
                       actor_id=request.user.id,
                       actor_name=request.user.username)
        celery_app.send_task(
            SchedulerCeleryTasks.JOBS_SCHEDULE_DELETION,
            kwargs={'job_id': obj.id, 'immediate': False},
            countdown=conf.get('GLOBAL_COUNTDOWN'))
        return Response(status=status.HTTP_200_OK)


class JobRestoreView(JobEndpoint, CreateEndpoint):
    """Restore an Build."""
    queryset = Job.all
    serializer_class = JobSerializer

    def post(self, request, *args, **kwargs):
        obj = self.get_object()
        auditor.record(event_type=JOB_RESTORED,
                       instance=obj,
                       actor_id=request.user.id,
                       actor_name=request.user.username)
        obj.restore()
        return Response(status=status.HTTP_200_OK)


class JobCloneView(JobEndpoint, CreateEndpoint):
    serializer_class = JobSerializer
    event_type = None

    def clone(self, obj, config, update_code_reference, description):
        pass

    def post(self, request, *args, **kwargs):
        ttl = self.request.data.get(RedisTTL.TTL_KEY)
        if ttl:
            try:
                ttl = RedisTTL.validate_ttl(ttl)
            except ValueError:
                raise ValidationError('ttl must be an integer.')

        auditor.record(event_type=self.event_type,
                       instance=self.job,
                       actor_id=self.request.user.id,
                       actor_name=self.request.user.username)

        description = None
        config = None
        update_code_reference = False
        if 'config' in request.data:
            spec = validate_job_spec_config(
                [self.job.specification.parsed_data, request.data['config']], raise_for_rest=True)
            config = spec.parsed_data
        if 'update_code' in request.data:
            try:
                update_code_reference = to_bool(request.data['update_code'])
            except TypeError:
                raise ValidationError('update_code should be a boolean')
        if 'description' in request.data:
            description = request.data['description']
        new_obj = self.clone(obj=self.job,
                             config=config,
                             update_code_reference=update_code_reference,
                             description=description)
        if ttl:
            RedisTTL.set_for_job(job_id=new_obj.id, value=ttl)
        serializer = self.get_serializer(new_obj)
        return Response(status=status.HTTP_201_CREATED, data=serializer.data)


class JobRestartView(JobCloneView):
    """Restart a job."""
    event_type = JOB_RESTARTED_TRIGGERED

    def clone(self, obj, config, update_code_reference, description):
        return obj.restart(user=self.request.user,
                           config=config,
                           update_code_reference=update_code_reference,
                           description=description)


class JobViewMixin(object):
    """A mixin to filter by job."""
    project = None
    job = None

    def get_job(self):
        # Get project and check access
        self.project = get_permissible_project(view=self)
        self.job = get_object_or_404(Job, project=self.project, id=self.kwargs['job_id'])
        return self.job

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        return queryset.filter(job=self.get_job())


class JobStatusListView(JobResourceListEndpoint, ListEndpoint, CreateEndpoint):
    """
    get:
        List all statuses of a job.
    post:
        Create a job status.
    """
    queryset = JobStatus.objects.order_by('created_at')
    serializer_class = JobStatusSerializer
    authentication_classes = api_settings.DEFAULT_AUTHENTICATION_CLASSES + [
        InternalAuthentication,
    ]

    def perform_create(self, serializer):
        serializer.save(job=self.job)

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        auditor.record(event_type=JOB_STATUSES_VIEWED,
                       instance=self.job,
                       actor_id=request.user.id,
                       actor_name=request.user.username)
        return response


class JobStatusDetailView(JobResourceEndpoint, RetrieveEndpoint):
    """Get job status details."""
    queryset = JobStatus.objects
    serializer_class = JobStatusSerializer
    lookup_field = 'uuid'
    lookup_url_kwarg = 'uuid'


class JobLogsView(JobEndpoint, RetrieveEndpoint):
    """Get job logs."""

    def get(self, request, *args, **kwargs):
        auditor.record(event_type=JOB_LOGS_VIEWED,
                       instance=self.job,
                       actor_id=request.user.id,
                       actor_name=request.user.username)
        job_name = self.job.unique_name
        if self.job.is_done:
            log_path = stores.get_job_logs_path(job_name=job_name, temp=False)
            log_path = archive_logs_file(
                log_path=log_path,
                namepath=job_name)
        else:
            process_logs(job=self.job, temp=True)
            log_path = stores.get_job_logs_path(job_name=job_name, temp=True)

        return stream_file(file_path=log_path, logger=_logger)


class JobStopView(JobEndpoint, PostEndpoint):
    """Stop a job."""

    def post(self, request, *args, **kwargs):
        auditor.record(event_type=JOB_STOPPED_TRIGGERED,
                       instance=self.job,
                       actor_id=request.user.id,
                       actor_name=request.user.username)
        celery_app.send_task(
            SchedulerCeleryTasks.JOBS_STOP,
            kwargs={
                'project_name': self.project.unique_name,
                'project_uuid': self.project.uuid.hex,
                'job_name': self.job.unique_name,
                'job_uuid': self.job.uuid.hex,
                'update_status': True,
                'collect_logs': True,
            },
            countdown=conf.get('GLOBAL_COUNTDOWN'))
        return Response(status=status.HTTP_200_OK)


class JobDownloadOutputsView(JobEndpoint, ProtectedView):
    """Download outputs of a job."""
    HANDLE_UNAUTHENTICATED = False

    def get(self, request, *args, **kwargs):
        auditor.record(event_type=JOB_OUTPUTS_DOWNLOADED,
                       instance=self.job,
                       actor_id=self.request.user.id,
                       actor_name=self.request.user.username)
        job_outputs_path = stores.get_job_outputs_path(
            persistence=self.job.persistence_outputs,
            job_name=self.job.unique_name)
        archived_path, archive_name = archive_outputs(
            outputs_path=job_outputs_path,
            name=self.job.unique_name)
        return self.redirect(path='{}/{}'.format(archived_path, archive_name))


class JobOutputsTreeView(JobEndpoint, RetrieveEndpoint):
    """
    get:
        Returns a the outputs directory tree.
    """
    def get(self, request, *args, **kwargs):
        try:
            store_manager = stores.get_outputs_store(
                persistence_outputs=self.job.persistence_outputs)
        except (PolyaxonStoresException, VolumeNotFoundError) as e:
            raise ValidationError(e)
        job_outputs_path = stores.get_job_outputs_path(
            persistence=self.job.persistence_outputs,
            job_name=self.job.unique_name)
        if request.query_params.get('path'):
            job_outputs_path = os.path.join(job_outputs_path,
                                            request.query_params.get('path'))

        try:
            data = store_manager.ls(job_outputs_path)
        except VolumeNotFoundError:
            raise ValidationError('Store manager could not load the volume requested,'
                                  ' to get the outputs data.')
        except Exception:
            raise ValidationError('Experiment outputs path does not exists or bad configuration.')
        return Response(data=data, status=200)


class JobOutputsFilesView(JobEndpoint, RetrieveEndpoint):
    """
    get:
        Returns a the outputs files content.
    """
    def get(self, request, *args, **kwargs):
        filepath = request.query_params.get('path')
        if not filepath:
            raise ValidationError('Files view expect a path to the file.')

        job_outputs_path = stores.get_job_outputs_path(
            persistence=self.job.persistence_outputs,
            job_name=self.job.unique_name)

        download_filepath = archive_outputs_file(persistence_outputs=self.job.persistence_outputs,
                                                 outputs_path=job_outputs_path,
                                                 namepath=self.job.unique_name,
                                                 filepath=filepath)
        if not download_filepath:
            return Response(status=status.HTTP_404_NOT_FOUND,
                            data='Outputs file not found: log_path={}'.format(download_filepath))

        return stream_file(file_path=download_filepath, logger=_logger)


class JobHeartBeatView(JobEndpoint, PostEndpoint):
    """
    post:
        Post a heart beat ping.
    """
    permission_classes = JobEndpoint.permission_classes + (IsAuthenticatedOrInternal,)
    authentication_classes = api_settings.DEFAULT_AUTHENTICATION_CLASSES + [
        InternalAuthentication,
    ]

    def post(self, request, *args, **kwargs):
        RedisHeartBeat.job_ping(job_id=self.job.id)
        return Response(status=status.HTTP_200_OK)


class JobImpersonateTokenView(JobEndpoint, PostEndpoint):
    """Impersonate a user and return user's token."""
    authentication_classes = [InternalAuthentication, ]
    permission_classes = (IsInitializer,)
    throttle_scope = 'impersonate'
    lookup_url_kwarg = 'job_id'

    def post(self, request, *args, **kwargs):
        job = self.get_object()

        if not JobLifeCycle.is_stoppable(job.last_status):
            return Response(status=status.HTTP_403_FORBIDDEN)

        token, _ = Token.objects.get_or_create(user=job.user)
        return Response({'token': token.key}, status=status.HTTP_200_OK)
