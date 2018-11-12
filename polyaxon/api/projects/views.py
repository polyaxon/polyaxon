from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

import auditor
from api.endpoint.base import ListEndpoint, RetrieveEndpoint, DestroyEndpoint, UpdateEndpoint
from api.endpoint.owner import OwnerEndpoint, OwnerResourceEndpoint
from api.endpoint.project import ProjectEndpoint

from api.projects import queries
from api.projects.serializers import (
    BookmarkedProjectSerializer,
    ProjectDetailSerializer,
    ProjectSerializer
)
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


class ProjectListView(OwnerResourceEndpoint, ListEndpoint):
    """List projects for a user."""
    queryset = queries.projects.order_by('-updated_at')
    serializer_class = BookmarkedProjectSerializer

    def filter_queryset(self, queryset):
        queryset = queryset.filter(owner=self.owner)
        if self.request.access.public_only:
            queryset = queryset.filter(is_public=True)
        return queryset


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
        'get': PROJECT_VIEWED,
        'update': PROJECT_UPDATED,
        'delete': PROJECT_DELETED_TRIGGERED,
    }
