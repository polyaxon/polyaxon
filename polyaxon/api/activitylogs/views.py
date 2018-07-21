from rest_framework.generics import ListAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated

from django.db.models import Q

import activitylogs

from api.activitylogs.serializers import ActivityLogsSerializer
from db.models.activitylogs import ActivityLog
from db.models.projects import Project


class HistoryLogsView(ListAPIView):
    """Activity logs list view."""
    # Filter only for user write events
    queryset = ActivityLog.objects.order_by('-created_at').filter(
        event_type__in=activitylogs.default_manager.user_view_events()
    )
    serializer_class = ActivityLogsSerializer
    permission_classes = (IsAuthenticated,)


class ActivityLogsView(ListAPIView):
    """Activity logs list view."""
    # Filter only for user write events
    queryset = ActivityLog.objects.order_by('-created_at').filter(
        event_type__in=activitylogs.default_manager.user_write_events()
    )
    serializer_class = ActivityLogsSerializer
    permission_classes = (IsAuthenticated,)


class ProjectActivityLogsView(ActivityLogsView):
    """Project activity logs list view."""

    def filter_queryset(self, queryset):
        project_name = self.kwargs['name']
        username = self.kwargs['username']
        project = get_object_or_404(Project, user__username=username, name=project_name)
        project_id = '{}'.format(project.id)
        # Filter for project/all events
        queryset = queryset.filter(
            Q(content_type__model='project', context__id=project_id) |
            Q(**{'context__project.id': project_id})
        )
        return super().filter_queryset(queryset=queryset)
