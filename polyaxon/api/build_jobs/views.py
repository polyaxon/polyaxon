import logging
import mimetypes
import os

from wsgiref.util import FileWrapper

from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import (
    CreateAPIView,
    RetrieveAPIView,
    RetrieveUpdateDestroyAPIView,
    get_object_or_404
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from django.http import StreamingHttpResponse

import auditor

from api.build_jobs.serializers import (
    BuildJobCreateSerializer,
    BuildJobDetailSerializer,
    BuildJobSerializer,
    BuildJobStatusSerializer
)
from api.utils.views import AuditorMixinView, ListCreateAPIView
from db.models.build_jobs import BuildJob, BuildJobStatus
from event_manager.events.build_job import (
    BUILD_JOB_CREATED,
    BUILD_JOB_DELETED_TRIGGERED,
    BUILD_JOB_LOGS_VIEWED,
    BUILD_JOB_STATUSES_VIEWED,
    BUILD_JOB_STOPPED_TRIGGERED,
    BUILD_JOB_UPDATED,
    BUILD_JOB_VIEWED
)
from event_manager.events.project import PROJECT_BUILDS_VIEWED
from libs.paths.jobs import get_job_logs_path
from libs.permissions.projects import get_permissible_project
from polyaxon.celery_api import app as celery_app
from polyaxon.settings import SchedulerCeleryTasks

from libs.repos.utils import get_project_latest_code_reference

_logger = logging.getLogger("polyaxon.views.builds")


class ProjectBuildListView(ListCreateAPIView):
    """List/Create an build under a project"""
    queryset = BuildJob.objects.all()
    serializer_class = BuildJobSerializer
    create_serializer_class = BuildJobCreateSerializer
    permission_classes = (IsAuthenticated,)

    def filter_queryset(self, queryset):
        project = get_permissible_project(view=self)
        auditor.record(event_type=PROJECT_BUILDS_VIEWED,
                       instance=project,
                       actor_id=self.request.user.id)
        return queryset.filter(project=project)

    def perform_create(self, serializer):
        project = get_permissible_project(view=self)
        code_reference = get_project_latest_code_reference(project=project)
        return serializer.save(user=self.request.user,
                               project=project,
                               code_reference=code_reference)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = self.perform_create(serializer)
        auditor.record(event_type=BUILD_JOB_CREATED, instance=instance)
        # Trigger build scheduling
        celery_app.send_task(
            SchedulerCeleryTasks.BUILD_JOBS_START,
            kwargs={'build_job_id': instance.id},
            countdown=1)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class BuildDetailView(AuditorMixinView, RetrieveUpdateDestroyAPIView):
    queryset = BuildJob.objects.all()
    serializer_class = BuildJobDetailSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'sequence'
    instance = None
    get_event = BUILD_JOB_VIEWED
    update_event = BUILD_JOB_UPDATED
    delete_event = BUILD_JOB_DELETED_TRIGGERED

    def filter_queryset(self, queryset):
        return queryset.filter(project=get_permissible_project(view=self))


class BuildViewMixin(object):
    """A mixin to filter by job."""
    project = None
    job = None

    def get_job(self):
        # Get project and check access
        self.project = get_permissible_project(view=self)
        sequence = self.kwargs['job_sequence']
        self.job = get_object_or_404(BuildJob, project=self.project, sequence=sequence)
        return self.job

    def filter_queryset(self, queryset):
        queryset = super(BuildViewMixin, self).filter_queryset(queryset)
        return queryset.filter(job=self.get_job())


class BuildStatusListView(BuildViewMixin, ListCreateAPIView):
    queryset = BuildJobStatus.objects.all()
    serializer_class = BuildJobStatusSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(job=self.get_job())

    def get(self, request, *args, **kwargs):
        response = super(BuildStatusListView, self).get(request, *args, **kwargs)
        auditor.record(event_type=BUILD_JOB_STATUSES_VIEWED,
                       instance=self.job,
                       actor_id=request.user.id)
        return response


class BuildStatusDetailView(BuildViewMixin, RetrieveAPIView):
    queryset = BuildJobStatus.objects.all()
    serializer_class = BuildJobStatusSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'uuid'


class BuildLogsView(BuildViewMixin, RetrieveAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        job = self.get_job()
        auditor.record(event_type=BUILD_JOB_LOGS_VIEWED,
                       instance=self.job,
                       actor_id=request.user.id)
        log_path = get_job_logs_path(job.unique_name)

        filename = os.path.basename(log_path)
        chunk_size = 8192
        try:
            wrapped_file = FileWrapper(open(log_path, 'rb'), chunk_size)
            response = StreamingHttpResponse(wrapped_file,
                                             content_type=mimetypes.guess_type(log_path)[0])
            response['Content-Length'] = os.path.getsize(log_path)
            response['Content-Disposition'] = "attachment; filename={}".format(filename)
            return response
        except FileNotFoundError:
            _logger.warning('Log file not found: log_path=%s', log_path)
            return Response(status=status.HTTP_404_NOT_FOUND,
                            data='Log file not found: log_path={}'.format(log_path))


class BuildStopView(CreateAPIView):
    queryset = BuildJob.objects.all()
    serializer_class = BuildJobSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'sequence'

    def filter_queryset(self, queryset):
        return queryset.filter(project=get_permissible_project(view=self))

    def post(self, request, *args, **kwargs):
        obj = self.get_object()
        auditor.record(event_type=BUILD_JOB_STOPPED_TRIGGERED,
                       instance=obj,
                       actor_id=request.user.id)
        celery_app.send_task(
            SchedulerCeleryTasks.BUILD_JOBS_STOP,
            kwargs={
                'project_name': obj.project.unique_name,
                'project_uuid': obj.project.uuid.hex,
                'build_job_name': obj.unique_name,
                'build_job_uuid': obj.unique_name,
                'specification': obj.specification,
                'update_status': True
            })
        return Response(status=status.HTTP_200_OK)
