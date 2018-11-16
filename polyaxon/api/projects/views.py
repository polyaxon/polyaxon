from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated

import auditor

from api.endpoint.base import DestroyEndpoint, ListEndpoint, RetrieveEndpoint, UpdateEndpoint
from api.endpoint.owner import OwnerProjectListPermission, OwnerResourceEndpoint
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
    PROJECT_CREATED,
    PROJECT_DELETED_TRIGGERED,
    PROJECT_UPDATED,
    PROJECT_VIEWED
)


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


class ProjectListView(BookmarkedListMixinView, OwnerResourceEndpoint, ListEndpoint):
    """List projects for a user."""
    queryset = queries.projects.order_by('-updated_at')
    permission_classes = (OwnerProjectListPermission,)
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
