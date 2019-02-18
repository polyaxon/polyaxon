from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth import get_user_model

import auditor

from api.archives.serializers import (
    ArchivedBuildJobSerializer,
    ArchivedExperimentGroupSerializer,
    ArchivedExperimentSerializer,
    ArchivedJobSerializer,
    ArchivedProjectSerializer
)
from api.endpoint.base import BaseEndpoint, ListEndpoint
from api.filters import OrderingFilter
from constants import content_types
from db.models.build_jobs import BuildJob
from db.models.experiment_groups import ExperimentGroup
from db.models.experiments import Experiment
from db.models.jobs import Job
from db.models.projects import Project
from event_manager.events.archive import (
    ARCHIVE_BUILD_JOBS_VIEWED,
    ARCHIVE_EXPERIMENT_GROUPS_VIEWED,
    ARCHIVE_EXPERIMENTS_VIEWED,
    ARCHIVE_JOBS_VIEWED,
    ARCHIVE_PROJECTS_VIEWED
)


class ArchiveListView(BaseEndpoint, ListEndpoint):
    """Base Archive list view."""
    permission_classes = (IsAuthenticated,)
    event_type = None
    content_type = None
    filter_backends = (OrderingFilter,)
    ordering = ('-updated_at',)
    ordering_fields = ('created_at', 'updated_at')

    def filter_queryset(self, queryset):
        username = self.kwargs['username']
        if self.request.user.username == username:
            user = self.request.user
        else:
            user = get_object_or_404(get_user_model(), username=username)
        should_access = (self.request.user.is_staff or
                         self.request.user.is_superuser
                         or self.request.user.username == username)
        if should_access:
            auditor.record(event_type=self.event_type,
                           instance=user,
                           actor_id=self.request.user.id,
                           actor_name=self.request.user.username)
            queryset = queryset.filter(user=user)
            return super().filter_queryset(queryset=queryset)
        return queryset.none()


class BuildArchiveListView(ArchiveListView):
    """List build bookmarks for a user."""
    queryset = BuildJob.archived
    event_type = ARCHIVE_BUILD_JOBS_VIEWED
    content_type = content_types.BUILD_JOB
    serializer_class = ArchivedBuildJobSerializer


class JobArchiveListView(ArchiveListView):
    """List job bookmarks for a user."""
    queryset = Job.archived
    event_type = ARCHIVE_JOBS_VIEWED
    content_type = content_types.JOB
    serializer_class = ArchivedJobSerializer


class ExperimentArchiveListView(ArchiveListView):
    """List experiment bookmarks for a user."""
    queryset = Experiment.archived
    event_type = ARCHIVE_EXPERIMENTS_VIEWED
    content_type = content_types.EXPERIMENT
    serializer_class = ArchivedExperimentSerializer


class ExperimentGroupArchiveListView(ArchiveListView):
    """List experiment group bookmarks for a user."""
    queryset = ExperimentGroup.archived
    event_type = ARCHIVE_EXPERIMENT_GROUPS_VIEWED
    content_type = content_types.EXPERIMENT_GROUP
    serializer_class = ArchivedExperimentGroupSerializer


class ProjectArchiveListView(ArchiveListView):
    """List project bookmarks for a user."""
    queryset = Project.archived
    event_type = ARCHIVE_PROJECTS_VIEWED
    content_type = content_types.PROJECT
    serializer_class = ArchivedProjectSerializer
