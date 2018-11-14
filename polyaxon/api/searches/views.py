import auditor

from api.endpoint.base import CreateEndpoint, DestroyEndpoint, ListEndpoint
from api.endpoint.project import ProjectResourceEndpoint, ProjectResourceListEndpoint
from api.filters import OrderingFilter
from api.paginator import LargeLimitOffsetPagination
from api.searches.serializers import SearchSerializer
from constants import content_types
from db.models.searches import Search
from event_manager.events.search import SEARCH_CREATED, SEARCH_DELETED


class SearchListView(ProjectResourceListEndpoint, ListEndpoint, CreateEndpoint):
    """Base Search list view."""
    queryset = Search.objects
    serializer_class = SearchSerializer
    content_type = None
    filter_backends = (OrderingFilter,)
    ordering = ('-updated_at',)
    ordering_fields = ('created_at', 'updated_at')
    pagination_class = LargeLimitOffsetPagination

    def filter_queryset(self, queryset):
        queryset = queryset.filter(user=self.request.user,
                                   content_type=self.content_type,
                                   project=self.project)
        return super().filter_queryset(queryset=queryset)

    def perform_create(self, serializer):
        instance = serializer.save(user=self.request.user,
                                   content_type=self.content_type,
                                   project=self.project)
        auditor.record(event_type=SEARCH_CREATED, instance=instance)


class BuildSearchListView(SearchListView):
    """List build searches for a user and a project."""
    content_type = content_types.BUILD_JOB


class JobSearchListView(SearchListView):
    """List job searches for a user and a project."""
    content_type = content_types.JOB


class ExperimentSearchListView(SearchListView):
    """List experiment searches for a user and a project."""
    content_type = content_types.EXPERIMENT


class ExperimentGroupSearchListView(SearchListView):
    """List experiment group searches for a user and project."""
    content_type = content_types.EXPERIMENT_GROUP


class SearchDeleteView(ProjectResourceEndpoint, DestroyEndpoint):
    """Base Search delete view."""
    lookup_field = 'id'
    queryset = Search.objects
    content_type = None

    def filter_queryset(self, queryset):
        return queryset.filter(user=self.request.user, project=self.project)

    def perform_destroy(self, instance):
        auditor.record(event_type=SEARCH_DELETED, instance=instance)
        super().perform_destroy(instance)


class BuildSearchDeleteView(SearchDeleteView):
    """Delete build search view."""
    content_type = content_types.BUILD_JOB


class JobSearchDeleteView(SearchDeleteView):
    """Delete job search view."""
    content_type = content_types.JOB


class ExperimentSearchDeleteView(SearchDeleteView):
    """Delete experiment search view."""
    content_type = content_types.EXPERIMENT


class ExperimentGroupSearchDeleteView(SearchDeleteView):
    """Delete experiment group search view."""
    content_type = content_types.EXPERIMENT_GROUP
