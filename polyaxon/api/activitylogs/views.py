from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from django.db.models import Q

from api.activitylogs.serializers import ActivityLogsSerializer
from db.models.activitylogs import ActivityLog


class ActivityLogsView(ListAPIView):
    """Activity logs list view."""
    queryset = ActivityLog.objects.order_by('-created_at')
    serializer_class = ActivityLogsSerializer
    permission_classes = (IsAuthenticated,)


class ProjectActivityLogsView(ListAPIView):
    """Project activity logs list view."""
    queryset = ActivityLog.objects.order_by('-created_at')
    serializer_class = ActivityLogsSerializer
    permission_classes = (IsAuthenticated,)

    def filter_queryset(self, queryset):
        project_id = '{}'.format(self.kwargs['id'])
        queryset = queryset.filter(
            Q(content_type__model='project', context__id=project_id) |
            Q(**{'context__project.id': project_id})
        )
        return super().filter_queryset(queryset=queryset)
