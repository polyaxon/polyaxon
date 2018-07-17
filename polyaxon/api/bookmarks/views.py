from rest_framework import status
from rest_framework.generics import DestroyAPIView, ListAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType

import auditor

from api.bookmarks.serializers import (
    BuildJobBookmarkSerializer,
    ExperimentBookmarkSerializer,
    ExperimentGroupBookmarkSerializer,
    JobBookmarkSerializer,
    ProjectBookmarkSerializer
)
from api.filters import OrderingFilter
from api.utils.views import PostAPIView
from db.models.bookmarks import Bookmark
from db.models.build_jobs import BuildJob
from db.models.experiment_groups import ExperimentGroup
from db.models.experiments import Experiment
from db.models.jobs import Job
from db.models.projects import Project
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
from libs.permissions.projects import IsProjectOwnerOrPublicReadOnly, get_permissible_project


class BookmarkListView(ListAPIView):
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
                           actor_id=self.request.user.id)
            queryset = queryset.filter(user=user, content_type__model=self.content_type)
            return super().filter_queryset(queryset=queryset)
        return queryset.none()


class BuildBookmarkListView(BookmarkListView):
    """List build bookmarks for a user."""
    event_type = BOOKMARK_BUILD_JOBS_VIEWED
    content_type = 'buildjob'
    serializer_class = BuildJobBookmarkSerializer


class JobBookmarkListView(BookmarkListView):
    """List job bookmarks for a user."""
    event_type = BOOKMARK_JOBS_VIEWED
    content_type = 'job'
    serializer_class = JobBookmarkSerializer


class ExperimentBookmarkListView(BookmarkListView):
    """List experiment bookmarks for a user."""
    event_type = BOOKMARK_EXPERIMENTS_VIEWED
    content_type = 'experiment'
    serializer_class = ExperimentBookmarkSerializer


class ExperimentGroupBookmarkListView(BookmarkListView):
    """List experiment group bookmarks for a user."""
    event_type = BOOKMARK_EXPERIMENT_GROUPS_VIEWED
    content_type = 'experimentgroup'
    serializer_class = ExperimentGroupBookmarkSerializer


class ProjectBookmarkListView(BookmarkListView):
    """List project bookmarks for a user."""
    event_type = BOOKMARK_PROJECTS_VIEWED
    content_type = 'project'
    serializer_class = ProjectBookmarkSerializer


class BookmarkCreateView(PostAPIView):
    """Base Bookmark create view."""
    permission_classes = (IsAuthenticated,)
    lookup_field = 'id'
    queryset = None
    event_type = None

    def filter_queryset(self, queryset):
        return queryset.filter(project=get_permissible_project(view=self))

    def create(self, request, *args, **kwargs):
        user = self.request.user
        obj = self.get_object()
        auditor.record(event_type=self.event_type,
                       instance=obj,
                       actor_id=user.id)
        bookmark, created = Bookmark.objects.get_or_create(
            user=user,
            content_type=ContentType.objects.get_for_model(obj),
            object_id=obj.id)
        if not created:
            bookmark.enabled = True
            bookmark.save()
        return Response(status=status.HTTP_201_CREATED)


class BookmarkDeleteView(DestroyAPIView):
    """Base Bookmark delete view."""
    permission_classes = (IsAuthenticated,)
    lookup_field = 'id'
    queryset = None
    event_type = None

    def filter_queryset(self, queryset):
        return queryset.filter(project=get_permissible_project(view=self))

    def destroy(self, request, *args, **kwargs):
        user = self.request.user
        obj = self.get_object()
        bookmark = get_object_or_404(Bookmark,
                                     user=user,
                                     content_type=ContentType.objects.get_for_model(obj),
                                     object_id=obj.id)
        auditor.record(event_type=self.event_type,
                       instance=obj,
                       actor_id=user.id)
        bookmark.enabled = False
        bookmark.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class BuildJobBookmarkCreateView(BookmarkCreateView):
    """Bookmark build view."""
    event_type = BUILD_JOB_BOOKMARKED
    queryset = BuildJob.objects.filter()


class BuildJobBookmarkDeleteView(BookmarkDeleteView):
    """Unbookmark build view."""
    event_type = BUILD_JOB_UNBOOKMARKED
    queryset = BuildJob.objects.filter()


class JobBookmarkCreateView(BookmarkCreateView):
    """Bookmark job view."""
    event_type = JOB_BOOKMARKED
    queryset = Job.objects.filter()


class JobBookmarkDeleteView(BookmarkDeleteView):
    """Unbookmark job view."""
    event_type = JOB_UNBOOKMARKED
    queryset = Job.objects.filter()


class ExperimentBookmarkCreateView(BookmarkCreateView):
    """Bookmark experiment view."""
    event_type = EXPERIMENT_BOOKMARKED
    queryset = Experiment.objects.filter()


class ExperimentBookmarkDeleteView(BookmarkDeleteView):
    """Unbookmark experiment view."""
    event_type = EXPERIMENT_UNBOOKMARKED
    queryset = Experiment.objects.filter()


class ExperimentGroupBookmarkCreateView(BookmarkCreateView):
    """Bookmark experiment group view."""
    event_type = EXPERIMENT_GROUP_BOOKMARKED
    queryset = ExperimentGroup.objects.filter()


class ExperimentGroupBookmarkDeleteView(BookmarkDeleteView):
    """Unbookmark experiment group view."""
    event_type = EXPERIMENT_GROUP_UNBOOKMARKED
    queryset = ExperimentGroup.objects.filter()


class ProjectBookmarkCreateView(BookmarkCreateView):
    """Bookmark project view."""
    event_type = PROJECT_BOOKMARKED
    queryset = Project.objects.filter()
    permission_classes = (IsAuthenticated, IsProjectOwnerOrPublicReadOnly)
    lookup_field = 'name'

    def filter_queryset(self, queryset):
        username = self.kwargs['username']
        return queryset.filter(user__username=username)


class ProjectBookmarkDeleteView(BookmarkDeleteView):
    """Unbookmark project view."""
    event_type = PROJECT_UNBOOKMARKED
    queryset = Project.objects.filter()
    permission_classes = (IsAuthenticated, IsProjectOwnerOrPublicReadOnly)
    lookup_field = 'name'

    def filter_queryset(self, queryset):
        username = self.kwargs['username']
        return queryset.filter(user__username=username)
