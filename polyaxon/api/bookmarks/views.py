from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from django.contrib.auth import get_user_model

import auditor

from api.bookmarks.serializers import (
    BuildJobBookmarkSerializer,
    ExperimentBookmarkSerializer,
    ExperimentGroupBookmarkSerializer,
    JobBookmarkSerializer,
    ProjectBookmarkSerializer
)
from api.endpoint.base import BaseEndpoint, DestroyEndpoint, ListEndpoint, PostEndpoint
from api.endpoint.build import BuildEndpoint
from api.endpoint.experiment import ExperimentEndpoint
from api.endpoint.group import ExperimentGroupEndpoint
from api.endpoint.job import JobEndpoint
from api.endpoint.project import ProjectEndpoint
from api.endpoint.public import PublicActivityPermission
from api.filters import OrderingFilter
from constants import content_types
from db.models.bookmarks import Bookmark
from event_manager.events.bookmark import (
    BOOKMARK_BUILD_JOBS_VIEWED,
    BOOKMARK_EXPERIMENT_GROUPS_VIEWED,
    BOOKMARK_EXPERIMENTS_VIEWED,
    BOOKMARK_JOBS_VIEWED,
    BOOKMARK_PROJECTS_VIEWED
)
from event_manager.events.build_job import BUILD_JOB_BOOKMARKED, BUILD_JOB_UNBOOKMARKED
from event_manager.events.experiment import EXPERIMENT_BOOKMARKED, EXPERIMENT_UNBOOKMARKED
from event_manager.events.experiment_group import (
    EXPERIMENT_GROUP_BOOKMARKED,
    EXPERIMENT_GROUP_UNBOOKMARKED
)
from event_manager.events.job import JOB_BOOKMARKED, JOB_UNBOOKMARKED
from event_manager.events.project import PROJECT_BOOKMARKED, PROJECT_UNBOOKMARKED


class BookmarkListView(BaseEndpoint, ListEndpoint):
    """Base Bookmark list view."""
    queryset = Bookmark.objects.all()
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
        if self.request.user.is_staff or self.request.user.username == username:
            auditor.record(event_type=self.event_type,
                           instance=user,
                           actor_id=self.request.user.id,
                           actor_name=self.request.user.username)
            queryset = queryset.filter(user=user,
                                       content_type__model=self.content_type,
                                       enabled=True)
            return super().filter_queryset(queryset=queryset)
        return queryset.none()


class BuildBookmarkListView(BookmarkListView):
    """List build bookmarks for a user."""
    event_type = BOOKMARK_BUILD_JOBS_VIEWED
    content_type = content_types.BUILD_JOB
    serializer_class = BuildJobBookmarkSerializer


class JobBookmarkListView(BookmarkListView):
    """List job bookmarks for a user."""
    event_type = BOOKMARK_JOBS_VIEWED
    content_type = content_types.JOB
    serializer_class = JobBookmarkSerializer


class ExperimentBookmarkListView(BookmarkListView):
    """List experiment bookmarks for a user."""
    event_type = BOOKMARK_EXPERIMENTS_VIEWED
    content_type = content_types.EXPERIMENT
    serializer_class = ExperimentBookmarkSerializer


class ExperimentGroupBookmarkListView(BookmarkListView):
    """List experiment group bookmarks for a user."""
    event_type = BOOKMARK_EXPERIMENT_GROUPS_VIEWED
    content_type = content_types.EXPERIMENT_GROUP
    serializer_class = ExperimentGroupBookmarkSerializer


class ProjectBookmarkListView(BookmarkListView):
    """List project bookmarks for a user."""
    event_type = BOOKMARK_PROJECTS_VIEWED
    content_type = content_types.PROJECT
    serializer_class = ProjectBookmarkSerializer


class BookmarkCreateView(BaseEndpoint, PostEndpoint):
    """Base Bookmark create view."""
    lookup_field = 'id'
    queryset = None
    event_type = None
    content_type = None
    permission_classes = (PublicActivityPermission,)

    def filter_queryset(self, queryset):
        if self.content_type == content_types.PROJECT:
            return super().filter_queryset(queryset)
        return queryset.filter(project=self.project)

    def create(self, request, *args, **kwargs):
        user = self.request.user
        obj = self.get_object()
        auditor.record(event_type=self.event_type,
                       instance=obj,
                       actor_id=user.id,
                       actor_name=user.username)
        try:
            bookmark = Bookmark.objects.get(
                user=user,
                content_type__model=self.content_type,
                object_id=obj.id)
            bookmark.enabled = True
            bookmark.save(update_fields=['enabled'])
        except Bookmark.DoesNotExist:
            Bookmark.objects.create(
                user=user,
                content_object=obj)
        return Response(status=status.HTTP_201_CREATED)


class BookmarkDeleteView(BaseEndpoint, DestroyEndpoint):
    """Base Bookmark delete view."""
    lookup_field = 'id'
    queryset = None
    event_type = None
    content_type = None
    permission_classes = (PublicActivityPermission,)

    def filter_queryset(self, queryset):
        if self.content_type == content_types.PROJECT:
            return super().filter_queryset(queryset)
        return queryset.filter(project=self.project)

    def destroy(self, request, *args, **kwargs):
        user = self.request.user
        obj = self.get_object()
        bookmark = get_object_or_404(Bookmark,
                                     user=user,
                                     content_type__model=self.content_type,
                                     object_id=obj.id)
        auditor.record(event_type=self.event_type,
                       instance=obj,
                       actor_id=user.id,
                       actor_name=user.username)
        bookmark.enabled = False
        bookmark.save(update_fields=['enabled'])
        return Response(status=status.HTTP_204_NO_CONTENT)


class BuildJobBookmarkCreateView(BuildEndpoint, BookmarkCreateView):
    """Bookmark build view."""
    event_type = BUILD_JOB_BOOKMARKED
    content_type = content_types.BUILD_JOB


class BuildJobBookmarkDeleteView(BuildEndpoint, BookmarkDeleteView):
    """Unbookmark build view."""
    event_type = BUILD_JOB_UNBOOKMARKED
    content_type = content_types.BUILD_JOB


class JobBookmarkCreateView(JobEndpoint, BookmarkCreateView):
    """Bookmark job view."""
    event_type = JOB_BOOKMARKED
    content_type = content_types.JOB


class JobBookmarkDeleteView(JobEndpoint, BookmarkDeleteView):
    """Unbookmark job view."""
    event_type = JOB_UNBOOKMARKED
    content_type = content_types.JOB


class ExperimentBookmarkCreateView(ExperimentEndpoint, BookmarkCreateView):
    """Bookmark experiment view."""
    event_type = EXPERIMENT_BOOKMARKED
    content_type = content_types.EXPERIMENT


class ExperimentBookmarkDeleteView(ExperimentEndpoint, BookmarkDeleteView):
    """Unbookmark experiment view."""
    event_type = EXPERIMENT_UNBOOKMARKED
    content_type = content_types.EXPERIMENT


class ExperimentGroupBookmarkCreateView(ExperimentGroupEndpoint, BookmarkCreateView):
    """Bookmark experiment group view."""
    event_type = EXPERIMENT_GROUP_BOOKMARKED
    content_type = content_types.EXPERIMENT_GROUP


class ExperimentGroupBookmarkDeleteView(ExperimentGroupEndpoint, BookmarkDeleteView):
    """Unbookmark experiment group view."""
    event_type = EXPERIMENT_GROUP_UNBOOKMARKED
    content_type = content_types.EXPERIMENT_GROUP


class ProjectBookmarkCreateView(ProjectEndpoint, BookmarkCreateView):
    """Bookmark project view."""
    event_type = PROJECT_BOOKMARKED
    content_type = content_types.PROJECT


class ProjectBookmarkDeleteView(ProjectEndpoint, BookmarkDeleteView):
    """Unbookmark project view."""
    event_type = PROJECT_UNBOOKMARKED
    content_type = content_types.PROJECT
