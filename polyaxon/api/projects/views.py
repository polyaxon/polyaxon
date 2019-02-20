from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

import auditor
import conf

from api.endpoint.admin import AdminProjectListPermission, AdminResourceEndpoint
from api.endpoint.base import (
    CreateEndpoint,
    DestroyEndpoint,
    ListEndpoint,
    RetrieveEndpoint,
    UpdateEndpoint
)
from api.endpoint.project import ProjectEndpoint
from api.projects import queries
from api.projects.serializers import (
    BookmarkedProjectSerializer,
    ProjectDetailSerializer,
    ProjectSerializer
)
from api.utils.views.bookmarks_mixin import BookmarkedListMixinView
from db.models.projects import Project
from event_manager.events.project import (
    PROJECT_ARCHIVED,
    PROJECT_CREATED,
    PROJECT_DELETED_TRIGGERED,
    PROJECT_RESTORED,
    PROJECT_UPDATED,
    PROJECT_VIEWED
)
from polyaxon.celery_api import celery_app
from polyaxon.settings import SchedulerCeleryTasks


class ProjectCreateView(CreateAPIView):
    """Create a project."""
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        project = serializer.validated_data['name']
        user = self.request.user
        if self.queryset.filter(user=user, name=project).count() > 0:
            raise ValidationError('A project with name `{}` already exists.'.format(project))
        instance = serializer.save(user=user)
        auditor.record(event_type=PROJECT_CREATED, instance=instance)


class ProjectListView(BookmarkedListMixinView, AdminResourceEndpoint, ListEndpoint):
    """List projects for a user."""
    queryset = queries.projects.order_by('-updated_at')
    permission_classes = (AdminProjectListPermission,)
    serializer_class = BookmarkedProjectSerializer

    def filter_queryset(self, queryset):
        if self.request.access.public_only:
            queryset = queryset.filter(is_public=True)
        return super().filter_queryset(queryset=queryset)


class ProjectDetailView(ProjectEndpoint, RetrieveEndpoint, UpdateEndpoint, DestroyEndpoint):
    """
    get:
        Get a project details.
    patch:
        Update a project details.
    delete:
        Delete a project.
    """
    queryset = queries.projects_details
    serializer_class = ProjectDetailSerializer
    AUDITOR_EVENT_TYPES = {
        'GET': PROJECT_VIEWED,
        'UPDATE': PROJECT_UPDATED,
        'DELETE': PROJECT_DELETED_TRIGGERED,
    }

    def perform_destroy(self, instance):
        instance.archive()
        celery_app.send_task(
            SchedulerCeleryTasks.PROJECTS_SCHEDULE_DELETION,
            kwargs={'project_id': instance.id, 'immediate': True},
            countdown=conf.get('GLOBAL_COUNTDOWN'))


class ProjectArchiveView(ProjectEndpoint, CreateEndpoint):
    """Restore an experiment."""
    serializer_class = ProjectSerializer

    def post(self, request, *args, **kwargs):
        obj = self.get_object()
        auditor.record(event_type=PROJECT_ARCHIVED,
                       instance=obj,
                       actor_id=request.user.id,
                       actor_name=request.user.username)
        celery_app.send_task(
            SchedulerCeleryTasks.PROJECTS_SCHEDULE_DELETION,
            kwargs={'project_id': obj.id, 'immediate': False},
            countdown=conf.get('GLOBAL_COUNTDOWN'))
        return Response(status=status.HTTP_200_OK)


class ProjectRestoreView(ProjectEndpoint, CreateEndpoint):
    """Restore an experiment."""
    queryset = Project.all
    serializer_class = ProjectSerializer

    def post(self, request, *args, **kwargs):
        obj = self.get_object()
        auditor.record(event_type=PROJECT_RESTORED,
                       instance=obj,
                       actor_id=request.user.id,
                       actor_name=request.user.username)
        obj.restore()
        return Response(status=status.HTTP_200_OK)
