import logging

from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.settings import api_settings

import auditor
import conf
import stores

from api.build_jobs import queries
from api.build_jobs.serializers import (
    BookmarkedBuildJobSerializer,
    BuildJobCreateSerializer,
    BuildJobDetailSerializer,
    BuildJobSerializer,
    BuildJobStatusSerializer
)
from api.endpoint.base import (
    CreateEndpoint,
    DestroyEndpoint,
    ListEndpoint,
    PostEndpoint,
    RetrieveEndpoint,
    UpdateEndpoint
)
from api.endpoint.build import BuildEndpoint, BuildResourceEndpoint, BuildResourceListEndpoint
from api.endpoint.project import ProjectResourceListEndpoint
from api.filters import OrderingFilter, QueryFilter
from api.utils.files import stream_file
from api.utils.views.bookmarks_mixin import BookmarkedListMixinView
from db.models.build_jobs import BuildJob, BuildJobStatus
from db.redis.heartbeat import RedisHeartBeat
from db.redis.tll import RedisTTL
from event_manager.events.build_job import (
    BUILD_JOB_ARCHIVED,
    BUILD_JOB_DELETED_TRIGGERED,
    BUILD_JOB_LOGS_VIEWED,
    BUILD_JOB_RESTORED,
    BUILD_JOB_STATUSES_VIEWED,
    BUILD_JOB_STOPPED_TRIGGERED,
    BUILD_JOB_UPDATED,
    BUILD_JOB_VIEWED
)
from event_manager.events.project import PROJECT_BUILDS_VIEWED
from libs.archive import archive_logs_file
from logs_handlers.log_queries.build_job import process_logs
from polyaxon.celery_api import celery_app
from polyaxon.settings import SchedulerCeleryTasks
from scopes.authentication.internal import InternalAuthentication
from scopes.permissions.internal import IsAuthenticatedOrInternal
from scopes.permissions.projects import get_permissible_project

_logger = logging.getLogger("polyaxon.views.builds")


class ProjectBuildListView(BookmarkedListMixinView,
                           ProjectResourceListEndpoint,
                           ListEndpoint,
                           CreateEndpoint):
    """
    get:
        List builds under a project.

    post:
        Create a build under a project.
    """
    queryset = queries.builds
    serializer_class = BookmarkedBuildJobSerializer
    create_serializer_class = BuildJobCreateSerializer
    filter_backends = (QueryFilter, OrderingFilter,)
    query_manager = 'build'
    ordering = ('-updated_at',)
    ordering_fields = ('created_at', 'updated_at', 'started_at', 'finished_at')

    def filter_queryset(self, queryset):
        auditor.record(event_type=PROJECT_BUILDS_VIEWED,
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
            RedisTTL.set_for_build(build_id=instance.id, value=ttl)
        # Trigger build scheduling
        celery_app.send_task(
            SchedulerCeleryTasks.BUILD_JOBS_START,
            kwargs={'build_job_id': instance.id},
            countdown=conf.get('GLOBAL_COUNTDOWN'))


class BuildDetailView(BuildEndpoint, RetrieveEndpoint, UpdateEndpoint, DestroyEndpoint):
    """
    get:
        Get a build details.
    patch:
        Update a build details.
    delete:
        Delete a build.
    """
    queryset = queries.builds_details
    serializer_class = BuildJobDetailSerializer
    AUDITOR_EVENT_TYPES = {
        'GET': BUILD_JOB_VIEWED,
        'UPDATE': BUILD_JOB_UPDATED,
        'DELETE': BUILD_JOB_DELETED_TRIGGERED
    }
    authentication_classes = api_settings.DEFAULT_AUTHENTICATION_CLASSES + [
        InternalAuthentication,
    ]

    def perform_destroy(self, instance):
        instance.archive()
        celery_app.send_task(
            SchedulerCeleryTasks.BUILD_JOBS_SCHEDULE_DELETION,
            kwargs={'build_job_id': instance.id, 'immediate': True},
            countdown=conf.get('GLOBAL_COUNTDOWN'))


class BuildArchiveView(BuildEndpoint, CreateEndpoint):
    """Restore an Build."""
    serializer_class = BuildJobSerializer

    def post(self, request, *args, **kwargs):
        obj = self.get_object()
        auditor.record(event_type=BUILD_JOB_ARCHIVED,
                       instance=obj,
                       actor_id=request.user.id,
                       actor_name=request.user.username)
        celery_app.send_task(
            SchedulerCeleryTasks.BUILD_JOBS_SCHEDULE_DELETION,
            kwargs={'build_job_id': obj.id, 'immediate': False},
            countdown=conf.get('GLOBAL_COUNTDOWN'))
        return Response(status=status.HTTP_200_OK)


class BuildRestoreView(BuildEndpoint, CreateEndpoint):
    """Restore an Build."""
    queryset = BuildJob.all
    serializer_class = BuildJobSerializer

    def post(self, request, *args, **kwargs):
        obj = self.get_object()
        auditor.record(event_type=BUILD_JOB_RESTORED,
                       instance=obj,
                       actor_id=request.user.id,
                       actor_name=request.user.username)
        obj.restore()
        return Response(status=status.HTTP_200_OK)


class BuildViewMixin(object):
    """A mixin to filter by job."""
    project = None
    job = None

    def get_job(self):
        # Get project and check access
        self.project = get_permissible_project(view=self)
        self.job = get_object_or_404(BuildJob, project=self.project, id=self.kwargs['job_id'])
        return self.job

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        return queryset.filter(job=self.get_job())


class BuildStatusListView(BuildResourceListEndpoint, ListEndpoint, CreateEndpoint):
    """
    get:
        List all statuses of a build.
    post:
        Create an build status.
    """
    queryset = BuildJobStatus.objects.order_by('created_at')
    serializer_class = BuildJobStatusSerializer
    authentication_classes = api_settings.DEFAULT_AUTHENTICATION_CLASSES + [
        InternalAuthentication,
    ]

    def perform_create(self, serializer):
        serializer.save(job=self.build)

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        auditor.record(event_type=BUILD_JOB_STATUSES_VIEWED,
                       instance=self.build,
                       actor_id=request.user.id,
                       actor_name=request.user.username)
        return response


class BuildStatusDetailView(BuildResourceEndpoint, RetrieveEndpoint):
    """Get build status details."""
    queryset = BuildJobStatus.objects
    serializer_class = BuildJobStatusSerializer
    lookup_field = 'uuid'
    lookup_url_kwarg = 'uuid'


class BuildLogsView(BuildEndpoint, RetrieveEndpoint):
    """Get build logs."""

    def get(self, request, *args, **kwargs):
        auditor.record(event_type=BUILD_JOB_LOGS_VIEWED,
                       instance=self.build,
                       actor_id=request.user.id,
                       actor_name=request.user.username)
        job_name = self.build.unique_name
        if self.build.is_done:
            log_path = stores.get_job_logs_path(job_name=job_name, temp=False)
            log_path = archive_logs_file(
                log_path=log_path,
                namepath=job_name)
        else:
            process_logs(build=self.build, temp=True)
            log_path = stores.get_job_logs_path(job_name=job_name, temp=True)

        return stream_file(file_path=log_path, logger=_logger)


class BuildStopView(BuildEndpoint, CreateEndpoint):
    """Stop a build."""
    serializer_class = BuildJobSerializer

    def post(self, request, *args, **kwargs):
        auditor.record(event_type=BUILD_JOB_STOPPED_TRIGGERED,
                       instance=self.build,
                       actor_id=request.user.id,
                       actor_name=request.user.username)
        celery_app.send_task(
            SchedulerCeleryTasks.BUILD_JOBS_STOP,
            kwargs={
                'project_name': self.project.unique_name,
                'project_uuid': self.project.uuid.hex,
                'build_job_name': self.build.unique_name,
                'build_job_uuid': self.build.uuid.hex,
                'update_status': True,
                'collect_logs': True,
            },
            countdown=conf.get('GLOBAL_COUNTDOWN'))
        return Response(status=status.HTTP_200_OK)


class BuildHeartBeatView(BuildEndpoint, PostEndpoint):
    """
    post:
        Post a heart beat ping.
    """
    permission_classes = BuildEndpoint.permission_classes + (IsAuthenticatedOrInternal,)
    authentication_classes = api_settings.DEFAULT_AUTHENTICATION_CLASSES + [
        InternalAuthentication,
    ]

    def post(self, request, *args, **kwargs):
        RedisHeartBeat.build_ping(build_id=self.build.id)
        return Response(status=status.HTTP_200_OK)
